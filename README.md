# The Download API for yt2mp3.ai

# How to download?
i mean its pretty fuckin straight forward but for those that dont know how to use python (how the hell do u know whats an API):

1. git clone https://github.com/turkishtutel/yt2mp3.ai-api
2. cd yt2mp3.-api
3. pip install requests
4. python api.py

and thats all ig

# How to use?

``` python
# dont touch these
TEST_VIDEO = input("Enter your youtube video ID (the thing after ?v=...): ")
FORMAT = input('"mp3" or "mp4": ')
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
```
``` python
# dont change anything
def getDownload():
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

    # fuckers changed the API, now for mp3 i need to get redirectURL
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
def getDownload():
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
        r1 = requests.get(convert_url, headers=headers, params=params) # calls the convertURL
        data = r1.json()
        redirect = data.get("redirectURL") # gets the redirect URL inside the response

        r = requests.get(redirect, headers=headers) # then moves on to get the download url
        data2 = r.json()

        return data2.get("downloadURL")
    elif FORMAT.lower() == "mp4":
        r = requests.get(convert_url, headers=headers, params=params) # pretty straightforward, convert url -> download url
        data = r.json()

        download_url = data.get("downloadURL")
        return download_url

```

## How to get the MP4/MP3?
``` python
# PS: add a 3 second delay before opening the URL like something like this

time.sleep(3)
print(download_url)
```

# Can I use this? And call it mine?

Yes and no, dont be a skid and call every project on github yours (you can call it yours if you actually contribute to this)
