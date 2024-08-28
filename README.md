## Getting Started

To get a local copy of the project up and running, follow these steps:


### Clone the repository:
    ```bash
    git clone https://github.com/LoySocheat/tele-bot-reels-poster.git
    ```

### Navigate to the project directory:

    ```bash
    cd tele-bot-reels-poster
    ```
## Run with Source Code

1. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Set up environment variables:**

    - Create a `.env` file in the root of your project directory. This file should contain environment-specific variables that your application needs. 
    - Example in`.env.example` file

3. **Run the script:**

    ```bash
    python ___init___.py
    ```

4. **Send the command `/start` to your bot on Telegram to start the process.**

## Run with Docker

1. **Docker pull the image:**

    ```bash
    sudo docker pull ghcr.io/loysocheat/tele-bot-reels-poster:v1.0
    ```

2. **Run with docker docker-compose:**

    ```bash
    sudo docker-compose up -d
    ```

3. **Send the command `/start` to your bot on Telegram to start the process.**

## License
Distributed under the MIT License. See `LICENSE` for more information.