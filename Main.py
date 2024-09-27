import yt_dlp

def download_video_yt_dlp(url):
    try:
        output_path = r'C:\Users\dhruv\Downloads\%(title)s.%(ext)s'

        ydl_opts = {
            'listformats': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        audio_formats = []
        video_formats = []

        for f in info['formats']:
            if f.get('ext') == 'mp4' and f.get('vcodec') != 'none':  # MP4 v formats
                video_formats.append(f)
            elif f.get('acodec') != 'none' and f.get('vcodec') == 'none':  # Audio formats
                audio_formats.append(f)

   
        print("\nAvailable formats:")
        idx = 1

        print("\n--- Video (mp4) ---")
        for video in video_formats:
            size = video.get('filesize', 'Unknown')
            print(f"{idx}. {video['format_id']} - {video.get('resolution')} ({size} bytes)")
            idx += 1

        print("\n--- Audio (mp3) ---")
        for audio in audio_formats:
            size = audio.get('filesize', 'Unknown')
            print(f"{idx}. {audio['format_id']} - mp3 ({size} bytes)")
            idx += 1


        format_index = int(input("\nEnter the number of the format you want to download: ")) - 1

 
        if format_index < len(video_formats):
            selected_format = video_formats[format_index]
        else:
            selected_format = audio_formats[format_index - len(video_formats)]
        
        selected_format_id = selected_format['format_id']

        ydl_opts = {
            'format': selected_format_id,
            'outtmpl': output_path,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ] if 'audio' in selected_format['acodec'] else []
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download successful!")

    except Exception as e:
        print(f"Error: {e}")

url = input("Enter the YouTube video URL: ")
download_video_yt_dlp(url)
