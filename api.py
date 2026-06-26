import requests
import time
from urllib.parse import urlparse, parse_qs

TEST_VIDEO = input("Enter your youtube video ID (the thing after ?v=...): ")
FORMAT = input('"mp3" or "mp4": ')
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
        "f": FORMAT,
        "_": ts
    }

    if FORMAT.lower() == "mp3":
        r1 = requests.get(convert_url, headers=headers, params=params)
        data = r1.json()
        redirect = data.get("redirectURL")

        r = requests.get(redirect, headers=headers)
        data2 = r.json()

        return data2.get("downloadURL")
    elif FORMAT.lower() == "mp4":
        r = requests.get(convert_url, headers=headers, params=params)
        data = r.json()

        download_url = data.get("downloadURL")
        return download_url

durl = getDownloadAndProgress()

print("Wait for the progress to finish.. (3 seconds)")
time.sleep(3)
print("download:", durl)
