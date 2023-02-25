import urllib.request

def is_img_file(url):
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    site = urllib.request.urlopen(url)
    meta = site.info()
    if "image/" in meta["content-type"]:
        return True
    return False

print(is_img_file("https://cdn.discordapp.com/attachments/882807640080674866/1072234438144037094/20230206_141622.jpg"))