import yt_dlp
import requests
import os, re
import time
import instaloader

# download video from YouTube
def download_youtube_video(youtube_url, save_path):
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            title = ydl.extract_info(youtube_url, download=False).get('title')
            description = ydl.extract_info(youtube_url, download=False).get('description').split("\n")[0]
            info_dict = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info_dict)
            return filename, title, description
    except Exception as e:
        print(f"Error downloading video from URL {youtube_url}: {str(e)}")
        return None

# download video from Tiktok
def download_tiktok_video(url, save_path):
    try:
        api_url = "https://www.tikwm.com/api/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        params = {"url": url}
        response = requests.get(api_url, headers=headers, params=params)
        data = response.json()

        if data['code'] == 0:
            video_data = data['data']
            video_download_url = video_data['play']
            video_title = video_data['title']
            
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            start = time.time()
            video_bytes = requests.get(video_download_url, stream=True)
            with open(f'{save_path}/{video_title}.mp4', 'wb') as out_file:
                out_file.write(video_bytes.content)
                end = time.time()

            elapsed_time = end - start
            print(f"[Programs] [Status] Timelapse: {elapsed_time:.2f}s")
            print(f"[Programs] [File] {video_title}.mp4 Downloaded")
            return f'{save_path}/{video_title}.mp4', video_title

        else:
            print("[Error] Failed to download TikTok video. Please check the URL and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

# download video from Instagram  
def download_instagram_reel(url, save_path):
    L = instaloader.Instaloader()
    try:
        shortcode = url.split('/')[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        caption = clean_caption(post.caption)
        if caption:
            sanitized_title = caption
        else:
            sanitized_title = shortcode
            
        if post.is_video:
            video_url = post.video_url
            start = time.time()
            video_bytes = requests.get(video_url, stream=True)
            with open(f'{save_path}/{sanitized_title}.mp4', 'wb') as out_file:
                out_file.write(video_bytes.content)
                end = time.time()
            elapsed_time = end - start
            print(f"[Programs] [Status] Timelapse: {elapsed_time:.2f}s")
            print(f"[Programs] [File] {sanitized_title}.mp4 Downloaded")
            return f'{save_path}/{sanitized_title}.mp4'
        else:
            print("[Error] Failed to download Instagram Reel. Please check the URL and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

# remove file
def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File {file_path} removed successfully.")
    else:
        print(f"File {file_path} not found.")  

# clean caption
def clean_caption(caption):
    caption = caption.replace("\n", " ")
    caption = re.sub(r'[\\/*?:"<>|]', "", caption)
    caption = re.sub(r'[.!?;,\[\](){}&%@$^*\'"\\]', "", caption)
    caption = re.sub(r'\s+', ' ', caption)
    caption = caption[:150]
    