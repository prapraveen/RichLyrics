import time
import os
from dotenv import load_dotenv
import requests
from discordrp import Presence
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pprint import pprint
from syrics.api import Spotify



load_dotenv()
discord_client_id = "1339009630734651461"
SP_DC = os.environ.get("SP_DC")
print(discord_client_id)

sp = Spotify(SP_DC)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
)

bearer_token = None

with open("accessToken.txt", "r") as file:
    content = file.read()
    bearer_token = content.strip()

    

@app.post("/send_token/{token}")
def receive_token(token: str):
    global bearer_token
    bearer_token = token
    prev_song_id = None
    lyrics = None
    with Presence(discord_client_id) as presence:
        while True:
            try:
                res = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": "Bearer " + bearer_token})
            except:
                time.sleep(2)
                continue
            if res.status_code != 200:
                print("not playing any song")
                time.sleep(1)
                continue
            data = res.json()
            song_id = data["item"]["id"]
            track_name = data["item"]["name"]
            artist_name = data["item"]["artists"][0]["name"]
            album_cover = data["item"]["album"]["images"][0]["url"]
            progress_ms = data["progress_ms"]
            duration_ms = data["item"]["duration_ms"]
            if song_id != prev_song_id or not lyrics:
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

"""
with Presence(discord_client_id) as presence:
    print("Connected")
    presence.set(
        {
            "state": "In Game",
            "details": "Summoner's Rift",
            "timestamps": {"start": int(time.time())},
        }
    )
    print("Presence updated")

    while True:
        time.sleep(15)
"""