# Team0-ImageBot

# Table of Contents
1. [Available Commands](#available-commands)
    1. [Meta Commands](#meta-commands)
    2. [Transformations](#transformations)
    3. [Color Filters](#color-filters)
    4. [Effects](#effects)
2. [Development Environment Setup](#development-environment-setup)

## Available Commands
All commands are prefixed with $. Additionally, note that the url argument is optional. By default, if no url is provided, then the most recently sent url in the channel is used.
### Meta Commands
1. `$help`
Provides a list of commands and arguments.
2. `$echo`
The bot echos back an image unchanged.
### Transformations
1. `$scale [factor] [url]`
Scales the provided image by the given amount. The factor must be positive. Additionally, neither height nor width of the resulting image can be greater than 65500 pixels.
2. `resize [width] [height] [url]`
Resizes the image to the given width and height. Likewise, neither height nor width of the resulting image can be greater than 65500 pixels.
3. `$rotate [degree] [url]`
Rotates the image by the given degrees counterclockwise. Negative values rotate clockwise
4. `$flip [direction] [url]`
If direction is 1, then the image is flipped vertically such that the top is at the bottom. If direction is 0, then the image is flipped horizontally.
5. `$compress [rate] [url]`
Compresses a JPEG by the specified rate between 0 and 1, inclusive. Image file size decreases as the compression rate goes down. Beware that information is lost during compression.
6. `$edge_detect [url]`
Converts the image to a black and white image, where edges detected in the original image are colored white.
### Color Filters
1. `$grayscale [url]`
Returns a grayscale version of the given image.
### Effects
1. `$triangulate [points] [url]`
Returns a triangulated version of an image.
    * `points` - integer in range [1, 16383) specifying how many samples from the image to take
2. `$tri_animate [url]`
Returns a gif with a triangulation effect.


### Image Drawing
1. `$pick_color [r] [g] [b]`
Picks the color to be used by future commands, given by the selected color channels, taking values between 0 and 255, inclusive. Note that values outside of this range with be taken modulo 256. It also sends back a swatch of the selected color.
2. `$sample_color [num_colors] [url]`
Picks the dominant color in the image to be used by future commands, given it is divided into the [num_colors] most dominant colors. This is accomplished using k-means clustering. It also sends back a swatch of the selected color.
3. `$line [x1] [y1] [x2] [y2] [width] [url]`
Draws a line from point (x1, y1) to (x2, y2) with the given width of the saved color. Arguments must be integers, and width must be positive. Note that the coordinates are given such that (0, 0) is in the top left corner
4. `$rect [x1] [y1] [x2] [y2] [width] [url]`
Draws a rectangle bounded by the points (x1, y1), (x2, y2) of the saved color.

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