#  Introduction to Video Upload Bot

This is a Telegram bot that allows users to upload videos to Facebook. The bot supports video files and URLs from YouTube, TikTok, and Instagram. Users can provide a title and description for the video, and the bot will handle the upload process to Facebook.

## How to Use
1. **Start a chat with the bot on Telegram.**
2. **Send your Facebook access token.**
3. **Share a video file or a URL (YouTube, TikTok, or Instagram).**
4. **Follow the bot's prompts to enter the title and description of the video.**
5. **The bot will handle the upload to Facebook and provide status updates throughout the process.**

## Getting Started

To get a local copy of the project up and running, follow these steps:


1. **Clone the repository:**
    
    ```bash
    git clone https://github.com/LoySocheat/tele-bot-reels-poster.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd tele-bot-reels-poster
    ```

3. **Set up environment variables:**

    - Create a `.env` file in the root of your project directory. This file should contain environment-specific variables that your application needs. 
    - Example in`.env.example` file

## Run with Source Code

1. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Run the script:**

    ```bash
    python ___init___.py
    ```

3. **Send the command `/start` to your bot on Telegram to start the process.**

## Run with Docker

1. **Docker pull the image:**

    ```bash
    sudo docker pull ghcr.io/loysocheat/tele-bot-reels-poster:v2.0
    ```

2. **Run with docker docker-compose:**

    ```bash
    sudo docker-compose up -d
    ```

3. **Send the command `/start` to your bot on Telegram to start the process.**