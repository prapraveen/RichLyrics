import time
import os
from dotenv import load_dotenv
import requests
from discordrp import Presence
from syrics.api import Spotify
import sys



load_dotenv()
discord_client_id = "1339009630734651461"
SP_DC = os.environ.get("SP_DC")

sp = Spotify(SP_DC)

access_code = input("Enter in your Spotify Access Code: ")
print("Setting Rich Presence!")
bearer_token_req = requests.get(f"https://rich-lyrics-api-4f1a2a064d31.herokuapp.com/get-access-token?code={access_code}")
if not bearer_token_req:
    print("Authentication did not work. Please try again.")
    print(bearer_token_req)
    print(bearer_token_req.json())
    sys.exit(1)

access_token = bearer_token_req.json()["access_token"]
refresh_token = bearer_token_req.json()["refresh_token"]
expiration_time = bearer_token_req.json()["expires_at"]

def get_new_token():
    global access_token, refresh_token, expiration_time
    res = requests.get(f"https://rich-lyrics-api-4f1a2a064d31.herokuapp.com/refresh-token?refresh_token={refresh_token}")
    if not res:
        print("Error refreshing token.")
        sys.exit(1)
    access_token = res.json()["access_token"]
    expiration_time = res.json()["expires_at"]

prev_song_id = None
lyrics = None
ends_at = None

with Presence(discord_client_id) as presence:
    while True:
        try:
            if time.time() * 1000 > expiration_time:
                get_new_token()
            res = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": "Bearer " + access_token})
        except:
            time.sleep(2)
            continue
        if res.status_code != 200:
            print("not playing any song")
            time.sleep(5)
            continue
        data = res.json()
        song_id = data["item"]["id"]
        track_name = data["item"]["name"]
        artist_name = data["item"]["artists"][0]["name"]
        album_cover = data["item"]["album"]["images"][0]["url"]
        progress_ms = data["progress_ms"]
        duration_ms = data["item"]["duration_ms"]
        if song_id != prev_song_id or not lyrics:
            ends_at = time.time() * 1000 + duration_ms
            lyrics = sp.get_lyrics(song_id)
            if not lyrics:
                print("error getting song lyrics")
                lyrics = None
                time.sleep(5)
                continue
            lyrics = lyrics["lyrics"]["lines"]
        
        idx = 0
        while progress_ms > int(lyrics[idx]["startTimeMs"]):
            idx += 1
            if idx == len(lyrics):
                break
        idx -= 1
        if idx < 0:
            lyric = ""
        else:
            lyric = lyrics[idx]["words"]

        presence.set(
            {
                "name": "listening to spotify",
                "type": 2,
                "assets": {"small_image": album_cover, 
                        "large_text": artist_name},
                "details": lyric if len(lyric) >= 3 else "♪♪♪",
                "state": track_name,
                "timestamps": {"start": int(time.time()) + progress_ms // 1000, "end": int(time.time()) + duration_ms // 1000}
            }
        )
        prev_song_id = song_id


        time.sleep(2)
