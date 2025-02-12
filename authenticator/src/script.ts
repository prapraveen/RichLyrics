// Because this is a literal single page application
// we detect a callback from Spotify by checking for the hash fragment
import { redirectToAuthCodeFlow } from "./authCodeWithPkce";

const clientId = "cb52476ef4c5422abfd747fb1bd8b701";
const params = new URLSearchParams(window.location.search);
const code = params.get("code");

if (!code) {
    redirectToAuthCodeFlow(clientId);
} else {
    displayAccessToken(code);
    // const accessToken = await getAccessToken(clientId, code);
    // displayAccessToken(accessToken);
    // await sendAccessToken(accessToken);
}

function displayAccessToken(token: string) {
    (document.querySelector("#access-token") as Element).innerHTML = `${token}`;
}

