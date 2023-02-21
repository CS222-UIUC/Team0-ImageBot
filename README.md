# Team0-ImageBot

## Development Environment Setup

1. Install Python 3.8 or higher

2. Clone the repository
    ```
    git clone https://github.com/CS222-UIUC/Team0-ImageBot
    ```
3. Set up your virtual environment
    ```
    cd Team0-ImageBot
    python3 -m venv bot-env
    ```
    Activate the virtual environment.

    (MacOS/Linux)
    ```
    source bot-env/bin/activate
    ```
    (Windows)
    ```
    bot-env\Scripts\activate.bat
    ```

4. Install necessary stuff
    ```
    pip install -r requirements.txt
    ```
    Be sure to update this file if you install a new library.

5. For testing locally, create a file called `BOT_TOKEN.txt`, and paste the bot token into there. 

    If hosting on Heroku, then go to the app's `Settings > Config Vars`. Add one with the key `"IMAGE_BOT_TOKEN"`, and put the bot token into the value.

6. To run the bot locally, run
    ```
    python3 main.py
    ```
    and `Ctrl+C` to stop.