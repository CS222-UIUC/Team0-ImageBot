Send these commands to the bot to test image link processing

1. Empty URL
    * `$test_image`
    * "Please send a URL linking to your image"

2. Not a URL
    * `$test_image a`
    * "URL was invalid, make sure to copy the image link"

3. Not a URL with image extension
    * `$test_image my_image.jpg`
    * "URL was invalid, make sure to copy the image link"

4. URL with non-image content type
    * `$test_image https://github.com/torvalds/linux`
    * "URL was invalid, make sure to copy the image link"

5. Image with extension in the URL
    * `$test_image https://imgs.xkcd.com/comics/computer_problems.png`
    * An XKCD comic

6. Image with no extension in the URL
    * `$test_image https://avatars.githubusercontent.com/u/1024025?v=4`
    * A picture of Linus Torvalds