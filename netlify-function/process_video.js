const { exec } = require('child_process');

exports.handler = async function(event, context) {
    const { url } = JSON.parse(event.body);

    if (!url) {
        return {
            statusCode: 400,
            body: JSON.stringify({ error: 'URL is required' }),  // Ensure this is valid JSON
        };
    }

    const ytDlpCommand = `yt-dlp -f best --no-warnings --quiet --extract-audio --audio-format mp3 ${url}`;

    try {
        exec(ytDlpCommand, (error, stdout, stderr) => {
            if (error) {
                return {
                    statusCode: 500,
                    body: JSON.stringify({ error: `Error: ${error.message}` }),  // Ensure this is valid JSON
                };
            }
            if (stderr) {
                return {
                    statusCode: 500,
                    body: JSON.stringify({ error: `stderr: ${stderr}` }),  // Ensure this is valid JSON
                };
            }

            // Assuming stdout contains the video URLs or download links
            const downloadLinks = stdout.split("\n").filter(link => link.includes('http'));

            return {
                statusCode: 200,
                body: JSON.stringify({ download_links: downloadLinks }),  // Ensure this is valid JSON
            };
        });
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: `Error: ${error.message}` }),  // Ensure this is valid JSON
        };
    }
};

