import requests
import urllib
r = requests.get("https://play.google.com/store/apps/details?id=com.facebook.katana")
from bs4 import BeautifulSoup
soup = BeautifulSoup(r.content)

img = soup.find("img",{"class":"cover-image"})["src"]
urllib.urlretrieve(img,"fb.jpg")