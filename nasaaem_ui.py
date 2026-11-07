"""Nasaaem Hospital UI theme for the synthetic Streamlit helpdesk."""
from pathlib import Path
import base64
import streamlit as st


def apply_nasaaem_theme():
    """Apply a light, accessible hospital-branded look without altering app logic."""
    logo_path = Path(__file__).resolve().parent / "assets" / "nasaaem_hospital_logo.png"
    logo_b64 = base64.b64encode(logo_path.read_bytes()).decode("ascii") if logo_path.exists() else ""
    watermark_css = (
        f'background-image: url("data:image/png;base64,{logo_b64}");'
        if logo_b64 else "background-image: none;"
    )
    st.markdown(
        """<style>
        :root { --nas-blue:#14588c; --nas-deep:#103e66; --nas-sky:#49a9d3;
                --nas-line:#d7e6f2; --nas-bg:#f3f8fd; }
        .stApp { background: linear-gradient(145deg, #f8fbff 0%, #edf6fd 100%);
                 color: #16324b; }
        .stApp::before {
            content:""; position:fixed; width:min(66vw,690px); height:min(46vh,420px);
            top:30%; left:50%; transform:translateX(-50%); z-index:0;
            """ + watermark_css + """
            background-repeat:no-repeat; background-position:center;
            background-size:contain; opacity:.085; pointer-events:none;
        }
        .stMainBlockContainer, [data-testid="stMainBlockContainer"] {
            position:relative; z-index:1;
            max-width:1200px; padding-top:2.5rem;
            padding-bottom:4rem;
        }
        h1, h2, h3 { color:#124a7b !important; letter-spacing:-.025em; }
        h1 { font-weight:800 !important; font-size:clamp(1.85rem,3.4vw,2.9rem) !important; }
        h2 { font-weight:750 !important; }
        p, label, [data-testid="stMarkdownContainer"] { line-height:1.6; }
        [data-testid="stForm"], [data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {
            border-color:#d9e7f3; border-radius:16px;
        }
        [data-testid="stForm"] {
            background:rgba(255,255,255,.91); border:1px solid #d9e7f3;
            box-shadow:0 12px 30px rgba(20,74,117,.06);
            padding:1.2rem;
        }
        .stButton > button[kind="primary"],
        .stFormSubmitButton > button,
        .stDownloadButton > button[kind="primary"] {
            background:linear-gradient(110deg,#176da9,#0c518c) !important;
            color:white !important; border:1px solid #176da9 !important;
            border-radius:11px !important; font-weight:700 !important;
            min-height:2.8rem;
            box-shadow:0 5px 12px rgba(20,88,140,.13);
        }
        .stButton > button:hover, .stFormSubmitButton > button:hover,
        .stDownloadButton > button:hover { border-color:#2387c4 !important; }
        .stButton > button, .stDownloadButton > button {
            border-radius:10px; min-height:2.65rem;
        }
        [data-baseweb="input"] > div, [data-baseweb="textarea"] > div {
            border-radius:10px !important; border-color:#c5dae9 !important;
        }
        [data-testid="stMetric"] { background:rgba(255,255,255,.9);
            border:1px solid var(--nas-line); border-radius:14px;
            padding:1rem 1.2rem; box-shadow:0 4px 14px rgba(20,74,117,.045); }
        [data-testid="stMetricValue"] { color:var(--nas-blue); }
        [data-testid="stDataFrame"] { border:1px solid var(--nas-line); border-radius:12px; overflow:hidden; }
        div[data-testid="stAlert"] { border-radius:11px; }
        [data-testid="stHorizontalBlock"] { align-items:stretch; }
        @media (max-width: 650px) {
          .stMainBlockContainer, [data-testid="stMainBlockContainer"] {
              padding:1.0rem .8rem 3rem !important;
          }
          .stApp::before { width:90vw; height:32vh; top:34%; opacity:.055; }
          h1 { font-size:1.8rem !important; }
          [data-testid="stForm"] { padding:.7rem; }
          .stButton button, .stFormSubmitButton button { min-height:3rem; }
        }
        </style>""",
        unsafe_allow_html=True,
    )
