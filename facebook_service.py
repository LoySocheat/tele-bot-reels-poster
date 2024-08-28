import os
import requests
from dotenv import load_dotenv

load_dotenv()

url_facebook_graph = os.getenv('URL_FACEBOOK_GRAPH')
verison_facebook_graph = os.getenv('VERISON_FACEBOOK_GRAPH')

def get_api_url(version=None):
    if version:
        return f'{url_facebook_graph}/{version}'
    return url_facebook_graph

# check access_token facebook
def handle_check_token(chat_id, token):
    url = f'{get_api_url(verison_facebook_graph)}/me?access_token={token}'
    response = requests.get(url)
    print(response.json().get('error', {}).get('message'))
    
    if response.status_code == 200:
        return True
    return False


# Helper function to create a reel on Facebook
def create_reel(access_token, video_path):
    try:
        url =  f'{get_api_url("v13.0")}/me/video_reels'
        params = {
            "access_token": access_token,
            "upload_phase": "start"
        }
        response = requests.post(url, params=params)
        if response.status_code == 200:
            jsonData = response.json()
            video_id = jsonData.get("video_id")
            if video_id:
                return upload_local_reel(video_id, video_path, access_token)
        return None
    except Exception as e:
        print(f"Error creating reel: {str(e)}")
        return None

# Helper function to upload a local reel to Facebook
def upload_local_reel(video_id, video_path, access_token):
    try:
        url = f"https://rupload.facebook.com/video-upload/v19.0/{video_id}"
        headers = {
            "Authorization": f"OAuth {access_token}",
            "Content-Type": "application/octet-stream",
            "offset": "0",
            "file_size": str(os.path.getsize(video_path))
        }
        with open(video_path, 'rb') as file:
            file_data = file.read()

        response = requests.post(url, headers=headers, data=file_data)
        if response.status_code == 200:
            return video_id
        else:
            print(f"Error uploading reel: {response.text}")
            return None
    except Exception as e:
        print(f"Error uploading reel: {str(e)}")
        return None

# Helper function to publish a reel to a Facebook page
def publish_reel_to_page(access_token, video_id, title, description):
    try:
        url = f"{get_api_url('v13.0')}/me/video_reels"
        params = {
            "access_token": access_token,
            "video_id": video_id,
            "upload_phase": "finish",
            "video_state": "PUBLISHED",
            "title": title,
            "description": description
        }
        response = requests.post(url, params=params)
        return response
    except Exception as e:
        print(f"Error publishing reel: {str(e)}")
        return None
