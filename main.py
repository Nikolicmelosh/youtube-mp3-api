from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Melosh YouTube to MP3 API is online and working."

@app.route('/mp3')
def mp3():
    url = request.args.get('url')
    user_filename = request.args.get('filename', 'download')

    if not url:
        return '❌ Missing "url" parameter', 400

    safe_filename = ''.join(c for c in user_filename if c.isalnum() or c in (' ', '-', '_')).rstrip()

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{safe_filename}.%(ext)s',
        'cookiefile': 'youtube.com_cookies.txt',
        'quiet': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'en-US,en;q=0.9',
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
        output_file = f"{safe_filename}.mp3"
        return send_file(output_file, as_attachment=True)
    except Exception as e:
        return f'❌ Download failed: {str(e)}', 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
