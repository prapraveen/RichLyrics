import './App.css'
import { useEffect, useState } from 'react';

function App() {
  const clientId = "cb52476ef4c5422abfd747fb1bd8b701";
  const params = new URLSearchParams(window.location.search);
  const code = params.get("code");
  const [access_code, setAccess_code] = useState(null)

  useEffect(() => {
    if (!code) {
      redirectToAuthCodeFlow(clientId);
    } else {
        setAccess_code(code)
        // const accessToken = await getAccessToken(clientId, code);
        // displayAccessToken(accessToken);
        // await sendAccessToken(accessToken);
    }
  }, [])
  

    
  return <>
    <h1>Your Spotify Code:</h1>
    <h2>{access_code}</h2>
    </>
}

export default App


async function redirectToAuthCodeFlow(clientId) {

  const params = new URLSearchParams();
  params.append("client_id", clientId);
  params.append("response_type", "code");
  params.append("redirect_uri", "http://localhost:5173/callback");
  params.append("scope", "user-read-playback-state");

  document.location = `https://accounts.spotify.com/authorize?${params.toString()}`;
}
