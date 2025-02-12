import requests
import base64
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

load_dotenv()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
print(spotify_client_id)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
)

@app.get("/get-access-token")
def get_access_token(code: str):
    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:5173/callback"
    }
    auth_header = base64.urlsafe_b64encode((spotify_client_id + ":" + spotify_client_secret).encode())
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": 'Basic %s' % auth_header.decode('ascii')
    }
    res = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=body).json()
    if "error" in res:
        return JSONResponse(status_code=400, content=res)
    
    res["expires_at"] = int(time.time() * 1000) + res["expires_in"] * 1000
    return res

@app.get("/refresh-token")
def refresh_token(refresh_token: str):
    client_creds = f"{spotify_client_id}:{spotify_client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

    headers = {
        "Authorization": f"Basic {client_creds_b64}"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    res = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
    if res.status_code == 200:
        data = res.json()
        data["expires_at"] = int(time.time() * 1000) + data["expires_in"] * 1000
        return data
    else:
        return JSONResponse(status_code=400, content=res.json())
