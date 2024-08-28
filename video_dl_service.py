import yt_dlp
import requests
import os
import time
import threading

def download_youtube_video(youtube_url, save_path):
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info_dict)
            return filename
    except Exception as e:
        print(f"Error downloading video from URL {youtube_url}: {str(e)}")
        return None

# download video from Tiktok
def tiktok_video(url, save_path):
    try:
        api_url = "https://www.tiktok.com/oembed"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        
        # change to when user downloaded to save_path
        params = {"url": url}
        response = requests.get(api_url, headers=headers, params=params)
        data = response.json()
        
        if data['code'] == 0:
            video_data = data['data']
            video_download_url = video_data['play']
            video_id = video_data['id']
            
            if not os.path.exists(save_path):
                os.makedirs(save_path)
                
            start = time.time()
            video_bytes = requests.get(video_download_url, stream=True)
            with open(f'{save_path}/{video_id}.mp4', 'wb') as out_file:
                out_file.write(video_bytes.content)
                end = time.time()
                
                elapsed_time = end - start
                print(f"Timelapse: {elapsed_time:.2f}s")
                print(f"File {video_id}.mp4 Downloaded")
                
                delay = 10
                timer = threading.Timer(delay, remove_file, args=[f'{save_path}/{video_id}.mp4'])
                timer.start()
        else:
            print("Failed to download video. Please check the URL and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File {file_path} removed successfully.")
    else:
        print(f"File {file_path} not found.")  