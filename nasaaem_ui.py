"""Nasaaem Hospital visual theme. No ticket, database or access-control logic."""
from pathlib import Path
import base64
import streamlit as st


def apply_nasaaem_theme():
    logo_path = Path(__file__).resolve().parent / "assets" / "nasaaem_hospital_logo.png"
    data_uri = (
        "data:image/png;base64," + base64.b64encode(logo_path.read_bytes()).decode("ascii")
        if logo_path.is_file() else ""
    )
    is_login = st.session_state.get("main_user") is None
    # Every CSS rule is inside exactly one <style> element. No CSS is sent as Markdown.
    css = r"""
<style>
:root { --nas-blue:#176aa4; --nas-navy:#104d7e; --nas-line:#d9e7f3; --nas-text:#183b57; }
.stApp { background:linear-gradient(135deg,#f9fcff,#edf6fd 70%,#e9f5fd); color:var(--nas-text); }
.stApp::before {
  content:""; position:fixed; inset:0; z-index:0; pointer-events:none;
  background-image:url("__LOGO_URI__"); background-repeat:no-repeat;
  background-size:min(58vw,600px) auto; background-position:center 57%; opacity:.052;
}
[data-testid="stMainBlockContainer"] {position:relative;z-index:1;max-width:1200px;padding-top:1.5rem;padding-bottom:3rem;}
h1,h2,h3 {color:var(--nas-navy)!important;letter-spacing:-.025em;}
[data-testid="stForm"], [data-testid="stMetric"] {background:rgba(255,255,255,.96);border:1px solid var(--nas-line);border-radius:20px;box-shadow:0 12px 38px rgba(17,81,129,.08);}
[data-testid="stForm"] {padding:1.4rem 1.6rem;}
[data-testid="stMetric"] {padding:1rem;}
[data-testid="stDataFrame"] {border:1px solid var(--nas-line);border-radius:14px;overflow:hidden;}
.stButton button,.stFormSubmitButton button,.stDownloadButton button {border-radius:11px!important;min-height:2.75rem;}
.stFormSubmitButton button[kind="primary"],.stButton button[kind="primary"] {background:#176aa4!important;color:white!important;border-color:#176aa4!important;}
[data-baseweb="input"]>div,[data-baseweb="textarea"]>div {border:1px solid #c9dfef!important;border-radius:10px!important;}
input,textarea {background:#f7fbff!important;}
[data-testid="stAlert"] {border-radius:12px;}
@media(max-width:650px) {
  [data-testid="stMainBlockContainer"] {padding:1rem .9rem 2rem!important;}
  .stApp::before {background-size:78vw auto;background-position:center 59%;opacity:.035;}
  [data-testid="stForm"] {padding:1rem!important;border-radius:17px!important;}
  .stButton button,.stFormSubmitButton button {min-height:3rem!important;}
}
</style>
"""
    if is_login:
        css += r"""
<style>
[data-testid="stMainBlockContainer"] {max-width:720px!important;margin:0 auto!important;padding-top:clamp(1.5rem,5vh,3rem)!important;}
[data-testid="stMainBlockContainer"] h1,[data-testid="stMainBlockContainer"] h2,[data-testid="stMainBlockContainer"] h3 {text-align:center!important;}
[data-testid="stMainBlockContainer"] h1 {font-size:clamp(1.85rem,3vw,2.35rem)!important;font-weight:800!important;}
[data-testid="stMainBlockContainer"] [data-testid="stCaptionContainer"] {text-align:center!important;color:#728ba1!important;}
[data-testid="stForm"] {max-width:540px!important;margin:0 auto!important;padding:1.4rem!important;}
[data-testid="stFormSubmitButton"] button {width:100%;min-height:48px!important;}
.nas-brand-hero {text-align:center!important;margin:0 auto 1.5rem!important;overflow:visible!important;}
.nas-brand-hero img {display:block!important;width:min(220px,60vw)!important;height:auto!important;max-height:none!important;object-fit:contain!important;margin:0 auto!important;}
@media(max-width:650px) {
  .nas-brand-hero img {width:min(175px,55vw)!important;}
  [data-testid="stMainBlockContainer"] h1 {font-size:1.8rem!important;}
}
</style>
"""
    css = css.replace("__LOGO_URI__", data_uri)
    st.html(css)
    if is_login and data_uri:
        st.html('<div class="nas-brand-hero"><img alt="Nasaaem Hospital" src="' + data_uri + '"></div>')
