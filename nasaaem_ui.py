"""Nasaaem Hospital premium UI presentation only; business logic unchanged."""
from pathlib import Path
import base64
import streamlit as st


def apply_nasaaem_theme():
    logo = Path(__file__).resolve().parent / 'assets' / 'nasaaem_hospital_logo.png'
    encoded = base64.b64encode(logo.read_bytes()).decode('ascii') if logo.is_file() else ''
    data_uri = 'data:image/png;base64,' + encoded if encoded else ''
    is_login = st.session_state.get('main_user') is None
    ui_class = 'nas-login' if is_login else 'nas-workspace'
    # The CSS applies to presentation only. It never changes application permissions/data.
    styles = r"""
    <style>
      :root {--nas-navy:#104c7d; --nas-blue:#176ba6; --nas-sky:#6abde7;
        --nas-ink:#173b59; --nas-muted:#657f94; --nas-border:#d9e7f3;}
      .stApp {background:linear-gradient(135deg,#fafcff 0%,#edf6fc 65%,#e8f4fc 100%);
        color:var(--nas-ink);}
      .stApp::before { content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
        background-image:url('LOGO_DATA_URL');background-size:min(64vw,710px) auto;
        background-position:center 63%;background-repeat:no-repeat;opacity:.045;}
      [data-testid="stMainBlockContainer"] {max-width:1200px;position:relative;z-index:1;
        padding-top:1rem;padding-bottom:3.5rem;}
      h1,h2,h3 {color:#104c7d!important;letter-spacing:-.025em;}
      h1{font-size:clamp(2rem,3.5vw,2.8rem)!important;font-weight:800!important;}
      h2{font-weight:750!important;}
      label,p{line-height:1.55;}
      .nas-brand-hero{text-align:center;margin:0 auto .65rem;max-width:720px;}
      .nas-brand-hero img{width:min(210px,52vw);max-height:170px;object-fit:contain;
        filter:drop-shadow(0 4px 7px rgba(23,107,166,.05));}
      .nas-brand-caption{font-size:.78rem;letter-spacing:.2em;font-weight:750;color:#246a9b;
        margin:.35rem 0 .15rem;}
      .nas-brand-rule{height:3px;width:80px;background:linear-gradient(90deg,#75c5e9,#18689f);
        border-radius:99px;margin:.9rem auto 0;}
      .nas-workspace-brand{display:flex;align-items:center;gap:.65rem;padding:.1rem 0 .35rem;}
      .nas-workspace-brand img{width:64px;height:45px;object-fit:contain;}
      .nas-workspace-brand span{font-size:.85rem;letter-spacing:.08em;font-weight:750;color:#195a8b;}
      [data-testid="stForm"]{background:rgba(255,255,255,.97);border:1px solid #d8e7f3;
        border-radius:21px;padding:1.5rem 1.7rem;
        box-shadow:0 22px 55px rgba(31,100,150,.11);}
      [data-testid="stVerticalBlockBorderWrapper"]{border-radius:17px;}
      [data-testid="stMetric"]{background:rgba(255,255,255,.95);
        border:1px solid var(--nas-border);border-radius:16px;
        padding:1rem 1.15rem;box-shadow:0 7px 24px rgba(29,88,130,.05);}
      [data-testid="stMetricValue"]{color:var(--nas-blue);}
      [data-testid="stDataFrame"]{border:1px solid var(--nas-border);border-radius:14px;overflow:hidden;}
      .stButton button,.stFormSubmitButton button,.stDownloadButton button{
        border-radius:12px!important;min-height:2.8rem;transition:background .2s,border-color .2s;}
      .stButton button[kind="primary"],.stFormSubmitButton button[kind="primary"]{
        background:linear-gradient(115deg,#1779b5,#105188)!important;color:#fff!important;
        border:1px solid #176da9!important;font-weight:700!important;
        box-shadow:0 8px 19px rgba(15,77,125,.15);}
      [data-baseweb="input"]>div,[data-baseweb="textarea"]>div{
        border:1px solid #c9dfef!important;border-radius:11px!important;}
      input,textarea{background-color:#f6fbff!important;}
      [data-testid="stAlert"]{border-radius:13px!important;}
      @media(max-width:650px){
        [data-testid="stMainBlockContainer"]{padding:1rem .85rem 3rem!important;}
        .nas-brand-hero img{width:min(155px,43vw);max-height:118px;}
        .nas-brand-caption{font-size:.69rem;}
        h1{font-size:1.9rem!important;}
        [data-testid="stForm"]{padding:1rem!important;border-radius:17px!important;}
        .stApp::before{background-size:80vw auto;background-position:center 55%;opacity:.035;}
        .stButton button,.stFormSubmitButton button{min-height:3rem!important;}
        [data-testid="stMetric"]{padding:.8rem!important;}
      }
    </style>"""
    styles = styles.replace('LOGO_DATA_URL', data_uri)
    # Scope login-only layout without relying on unstable CSS :has() selectors.
    if is_login:
        styles += """<style>
         [data-testid='stForm']{max-width:620px;margin-inline:auto;}
         [data-testid='stMainBlockContainer']{max-width:1000px;padding-top:1.1rem;}
         h1,h2{text-align:center;}
         [data-testid='stFormSubmitButton'] button{width:100%;}
         @media(max-width:650px){h2{font-size:1.4rem!important;}}
        </style>"""
    st.markdown(styles, unsafe_allow_html=True)
    if is_login:
        st.markdown(
            '<div class="nas-brand-hero">'
            + (f'<img src="{data_uri}" alt="Nasaaem Hospital logo">' if data_uri else '')
            + '<div class="nas-brand-caption">NASAAEM HOSPITAL</div>'
            + '<div class="nas-brand-rule"></div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="nas-workspace-brand">'
            + (f'<img src="{data_uri}" alt="Nasaaem Hospital logo">' if data_uri else '')
            + '<span>NASAAEM HOSPITAL · HELPDESK</span></div>',
            unsafe_allow_html=True,
        )
