Send these commands to the bot to test image link processing

1. Empty URL
    * `$hue`
    * "Usage: $hue [change] [url]. Hue change is between 0 and 180."

2. Not a URL
    * `$hue a`
    * "Usage: $hue [change] [url]. Hue change is between 0 and 180."

3. Not a URL with image extension
    * `$hue my_image.jpg`
    * "Usage: $hue [change] [url]. Hue change is between 0 and 180."

4. URL with valid hue change
    * `$hue 90 https://cdn.discordapp.com/attachments/882807640080674866/1072234438144037094/20230206_141622.jpg`
    * A hue shifted picture

5. URL with invalid hue change
    * `$hue 200 https://cdn.discordapp.com/attachments/882807640080674866/1072234438144037094/20230206_141622.jpg`
    * "Hue change is between 0 and 180."

6. Not a URL with hue change
    * `$hue 20 my_image.jpg`
    * "Hue change is between 0 and 180."

7. Not a URL with non-integer hue change
    * `$hue test my_image.jpg`
    * "Hue change is between 0 and 180."

8. Not a URL with invalid hue change
    * `$hue 300 my_image.jpg`
    * "Hue change is between 0 and 180."

9. URL with non-integer hue change
    * `$hue test https://cdn.discordapp.com/attachments/882807640080674866/1072234438144037094/20230206_141622.jpg`
    * "Hue change is integer between 0 and 180."