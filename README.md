# Team0-ImageBot

# Table of Contents
1. [Available Commands](#available-commands)
    1. [Transformations](#transformations)
    2. [Color Filters](#color-filters)
2. [Development Environment Setup](#development-environment-setup)

## Available Commands
All commands are prefixed with $.
1. `$help`
Provides a list of commands and arguments
### Transformations
1. `$scale [factor] [url]`
Scales the provided image by the given amount. The factor must be positive. Additionally, neither height nor width of the resulting image can be greater than 65500 pixels.
2. `resize [width] [height] [url]`
Resizes the image to the given width and height. Likewise, neither height nor width of the resulting image can be greater than 65500 pixels.
3. `$rotate [degree] [url]`
Rotates the image by the given degrees counterclockwise. Negative values rotate clockwise
4. `$flip [direction] [url]`
If direction is 1, then the image is flipped vertically such that the top is at the bottom. If direction is 0, then the image is flipped horizontally.
### Color Filters
5. `$grayscale [url]`
Returns a grayscale version of the given image.

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