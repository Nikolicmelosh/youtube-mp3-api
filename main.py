from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ YouTube to MP3 API is running."

@app.route('/mp3')
def mp3():
    url = request.args.get('url')
    user_filename = request.args.get('filename', 'download')  # default to "download"

    if not url:
        return '❌ Missing URL', 400

    safe_filename = ''.join(c for c in user_filename if c.isalnum() or c in (' ', '-', '_')).rstrip()

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{safe_filename}.%(ext)s',
        'cookiefile': 'youtube_cookies.txt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            output_file = f"{safe_filename}.mp3"

        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return f'❌ Error: {str(e)}', 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
