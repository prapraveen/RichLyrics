(function(){const o=document.createElement("link").relList;if(o&&o.supports&&o.supports("modulepreload"))return;for(const e of document.querySelectorAll('link[rel="modulepreload"]'))n(e);new MutationObserver(e=>{for(const t of e)if(t.type==="childList")for(const c of t.addedNodes)c.tagName==="LINK"&&c.rel==="modulepreload"&&n(c)}).observe(document,{childList:!0,subtree:!0});function i(e){const t={};return e.integrity&&(t.integrity=e.integrity),e.referrerPolicy&&(t.referrerPolicy=e.referrerPolicy),e.crossOrigin==="use-credentials"?t.credentials="include":e.crossOrigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function n(e){if(e.ep)return;e.ep=!0;const t=i(e);fetch(e.href,t)}})();async function a(r){const o=new URLSearchParams;o.append("client_id",r),o.append("response_type","code"),o.append("redirect_uri","http://localhost:5173/callback"),o.append("scope","user-read-playback-state"),document.location=`https://accounts.spotify.com/authorize?${o.toString()}`}const d="cb52476ef4c5422abfd747fb1bd8b701",l=new URLSearchParams(window.location.search),s=l.get("code");s?u(s):a(d);function u(r){document.querySelector("#access-token").innerHTML=`${r}`}
