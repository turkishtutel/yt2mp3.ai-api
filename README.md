## The Download API for yt2mp3.ai

# How to download?
i mean its pretty fuckin straight forward but for those that dont know how to use python (how the hell do u know whats an API):

0.git clone https://github.com/turkishtutel/yt2mp3.ai-api**
0.1. cd yt2mp3.-api
1. pip install requests
2. python api.py

and thats all ig

# How to use?

``` python
# dont touch these
TEST_VIDEO = input("Enter your youtube video ID (the thing after ?v=...): ")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
```
``` python
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
        "f": "mp3", # change this to mp4 if you want .mp4 file format(all lowercase)
        "_": ts
    }

    r = requests.get(convert_url, headers=headers, params=params)

    data = r.json()

    download_url = data.get("downloadURL")
    progress_url = data.get("progressURL")

    return download_url, progress_url
```

# How does it work? Every function explained apart

## Getting the authorization key
``` python
def getKey():
    ts = int(time.time() * 1000) # timestamp to prove non-botness

    # headers that the API needs to work
    headers = { 
        "User-Agent": UA, 
        "Origin": "https://yt2mp3.ai",
        "Referer": "https://yt2mp3.ai/"
    }

    # to get the key
    r = requests.get(
        f"https://gamma.gammacloud.net/api/v1/auth?_={ts}",
        headers=headers
    )

    data = r.json()
    return data["key"]
```

## Getting the URL for conversion
``` python
def getConvertURL():
    ts = int(time.time() * 1000)

    headers = {
        "User-Agent": UA,
        "Authorization": "Bearer " + getKey(), # use from the last function the key, this will be used 1 time, for the init api
        "Origin": "https://yt2mp3.ai",
        "Referer": "https://yt2mp3.ai/"
    } 
    # initialize the convert URL
    r = requests.get(
        f"https://gamma.gammacloud.net/api/v1/init?_={ts}",
        headers=headers
    )

    data = r.json()
    return data["convertURL"]
```

## Getting the ?sig=... from a url (for our case, from our convertURL)
``` python
def getSig(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    return params.get("sig", [None])[0]
```

## Actually getting the Download API
``` python
def getDownloadAndProgress():
    ts = int(time.time() * 1000)

    convert_url = getConvertURL()
    sig = getSig(convert_url)

    headers = {
        "User-Agent": UA,
        "Origin": "https://yt2mp3.ai",
        "Referer": "https://yt2mp3.ai/"
    }

    # parameters to authorize and get the downloadURL from the convertURL, since it probably returns something like
    # { "downloadURL" : "https://...", "errors": 0, "progressURL": "https://...", "title": null }
    params = {
        "sig": sig, # isnt optional
        "v": TEST_VIDEO, #isnt optional either
        "f": "mp3", # as i said, change to mp4 all lowercase if you want mp4 format instead
        "_": ts # timestamp
    }

    r = requests.get(convert_url, headers=headers, params=params) 

    data = r.json()

    download_url = data.get("downloadURL") # you only need this anyways
    progress_url = data.get("progressURL")

    return download_url, progress_url
```

## How to get the MP4/MP3?
``` python
# PS: i have no idea on automatically but im showing you the link way
print(download_url)
```

# Can I use this? And call it mine?

Yes and no, dont be a skid and call every project on github yours (you can call it yours if you actually contribute to this)
