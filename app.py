import yt_dlp as youtube_dl
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return "Flask Backend is Running!"

# Function to get direct download link from YouTube URL (including playlists)
def get_video_download_link(url):
    try:
        ydl_opts = {
            'format': 'best',  # Download best quality video
            'outtmpl': 'downloads/%(id)s.%(ext)s',  # Save video to this path
            'quiet': True,
            'no_warnings': True,
            'force_generic_extractor': True,
            'extract_flat': False,  # Actually download video, not just URLs
            'noplaylist': False,  # Allow playlist extraction
        }

        # Use yt-dlp to process playlist or single video URL
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)  # Download the videos

            # If the URL is a playlist, extract all video download links
            if 'entries' in info_dict:
                video_urls = []
                for entry in info_dict['entries']:
                    video_urls.append(entry['url'])  # Use the download URL
                return video_urls
            else:
                # Single video URL
                return [info_dict['url']]  # Return direct video file URL
    except Exception as e:
        print(f"Error fetching video: {e}")  # Log the error for debugging
        return str(e)

@app.route('/process_video', methods=['POST'])
def process_video():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({"error": "URL is required"}), 400

    download_links = get_video_download_link(video_url)
    if "error" in download_links:
        return jsonify({"error": "Failed to fetch the video. Please check the URL."}), 500

    return jsonify({"download_links": download_links})

if __name__ == '__main__':
    app.run(debug=True)
