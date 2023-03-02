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

7. Image that requires a user-agent to be set
    * `$test_image https://cdn.discordapp.com/attachments/882807640080674866/1072234438144037094/20230206_141622.jpg`
    * A stack of crewmate action figures (should not be a 403 error)

8. Image with long filename
    * `$test_image https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.survivethenews.com%2Fwp-content%2Fuploads%2F2022%2F08%2F1659378236_411_Reuters-Runs-Cover-for-Dementia-Joe-and-%25E2%2580%2598Fact-Checks-Funny-Meme.jpg&f=1&nofb=1&ipt=402b35a33f341c13a4c8c4b8553448c15f6296581479667007462ce2e6471a09&ipo=images`
    * Joe Biden eating ice cream