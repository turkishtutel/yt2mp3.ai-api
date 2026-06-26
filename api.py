import requests
import time
from urllib.parse import urlparse, parse_qs

TEST_VIDEO = input("Enter your youtube video ID (the thing after ?v=...): ")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"

def getKey():
    ts = int(time.time() * 1000)

    headers = {
        "User-Agent": UA,
        "Origin": "https://yt2mp3.ai",
        "Referer": "https://yt2mp3.ai/"
    }

    r = requests.get(
        f"https://gamma.gammacloud.net/api/v1/auth?_={ts}",
        headers=headers
    )

    data = r.json()
    return data["key"]

def getConvertURL():
    ts = int(time.time() * 1000)

    headers = {
        "User-Agent": UA,
        "Authorization": "Bearer " + getKey(),
        "Origin": "https://yt2mp3.ai",
        "Referer": "https://yt2mp3.ai/"
    }

    r = requests.get(
        f"https://gamma.gammacloud.net/api/v1/init?_={ts}",
        headers=headers
    )

    data = r.json()
    return data["convertURL"]

def getSig(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    return params.get("sig", [None])[0]

def getDownloadAndProgress():
    ts = int(time.time() * 1000)

    convert_url = getConvertURL()
    sig = getSig(convert_url)

    headers = {
        "User-Agent": UA,
        "Origin": "https://yt2mp3.ai",
        "Referer": "https://yt2mp3.ai/"
    }

    params = {
        "sig": sig,
        "v": TEST_VIDEO,
        "f": "mp3",
        "_": ts
    }

    r = requests.get(convert_url, headers=headers, params=params)

    data = r.json()

    download_url = data.get("downloadURL")
    progress_url = data.get("progressURL")

    return download_url, progress_url

durl, purl = getDownloadAndProgress()

print("download:", durl)
print("progress:", purl)
