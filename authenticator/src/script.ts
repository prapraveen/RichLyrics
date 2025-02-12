// Because this is a literal single page application
// we detect a callback from Spotify by checking for the hash fragment
import { redirectToAuthCodeFlow, getAccessToken } from "./authCodeWithPkce";

const clientId = "cb52476ef4c5422abfd747fb1bd8b701";
const params = new URLSearchParams(window.location.search);
const code = params.get("code");

if (!code) {
    redirectToAuthCodeFlow(clientId);
} else {
    const accessToken = await getAccessToken(clientId, code);
    displayAccessToken(accessToken);
    await sendAccessToken(accessToken);
}

function displayAccessToken(token: string) {
    (document.querySelector("#access-token") as Element).innerHTML = `${token}`;
}

async function sendAccessToken(code: string): Promise<UserProfile> {
    console.log(code);
    const requestOptions = {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
    }
    const result = await fetch(`http://127.0.0.1:8000/send_token/${code}`, requestOptions);

    return await result.json();
}

