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
    # NASAAEM_LOGIN_POLISH_609 — login-only enhancements, no backend changes
    if is_login:
        styles += r"""
        <style>
          [data-testid="stMainBlockContainer"] {
            max-width: 620px !important;
            padding-top: clamp(1.4rem, 5vh, 3rem) !important;
            padding-bottom: 2rem !important;
          }
          .nas-brand-hero { margin: 0 auto .55rem !important; }
          .nas-brand-hero img {
            width: min(190px, 48vw) !important;
            height: auto !important;
            max-height: none !important;
            object-fit: contain !important;
          }
          .nas-brand-caption { display: none !important; }
          .nas-brand-rule { margin: .65rem auto .5rem !important; width: 56px !important; }
          h1 { text-align: center !important; font-size: clamp(1.75rem, 3vw, 2.15rem) !important; margin-top: .1rem !important; }
          h2, h3 { text-align: center !important; }
          [data-testid="stForm"] {
            margin: .6rem auto .15rem !important;
            max-width: 560px !important;
            padding: 1.35rem 1.5rem !important;
            border-radius: 22px !important;
            box-shadow: 0 12px 36px rgba(17,81,129,.10) !important;
          }
          [data-testid="stMainBlockContainer"] > div > div > div { min-width: 0; }
          .stApp::before { opacity: .028 !important; background-position: center 66% !important; }
          [data-testid="stCaptionContainer"] { text-align: center; }
          @media (max-width: 650px) {
            [data-testid="stMainBlockContainer"] { padding: 1.25rem 1rem 2rem !important; }
            .nas-brand-hero img { width: min(155px, 45vw) !important; }
            [data-testid="stForm"] { padding: 1.1rem !important; border-radius: 18px !important; }
            h1 { font-size: 1.7rem !important; }
          }
        </style>
        """
    # NASAAEM_LOGIN_POLISH_617 — presentation only, no backend changes.
    if is_login:
        styles += """<style>
        /* Deliberate visual hierarchy: one logo, one title and one login card. */
        [data-testid="stMainBlockContainer"] {
          max-width: 720px !important;
          padding-top: clamp(3rem, 7vh, 5rem) !important;
          padding-bottom: 2rem !important;
          margin-inline: auto !important;
        }
        .nas-brand-hero { margin: 0 auto .75rem !important; padding-top: 1rem !important; overflow: visible !important; text-align:center !important; }
        .nas-brand-hero img {
          display: block !important;
          width: min(190px, 48vw) !important;
          height: auto !important;
          max-height: none !important;
          object-fit: contain !important;
          margin: 0 auto !important;
        }
        /* The official image already contains NASAAEM HOSPITAL. */
        .nas-brand-caption, .nas-brand-rule { display:none !important; }
        [data-testid="stMainBlockContainer"] h1 {
          text-align:center !important;
          font-size: clamp(1.75rem, 3vw, 2.25rem) !important;
          letter-spacing: -.035em !important;
          line-height: 1.16 !important;
          margin: .25rem 0 0 !important;
          font-weight: 800 !important;
        }
        [data-testid="stMainBlockContainer"] h2,
        [data-testid="stMainBlockContainer"] h3 {
          text-align:center !important;
          font-size: clamp(1.05rem, 2vw, 1.25rem) !important;
          font-weight: 650 !important;
          margin: .15rem 0 0 !important;
        }
        [data-testid="stMainBlockContainer"] [data-testid="stCaptionContainer"] {
          text-align:center !important;
          color:#657d92 !important;
          font-size:.86rem !important;
        }
        [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] {
          row-gap: .65rem;
        }
        [data-testid="stForm"] {
          width: min(100%, 540px) !important;
          max-width: 540px !important;
          margin: .25rem auto 0 !important;
          padding: clamp(1.15rem,2.5vw,1.8rem) !important;
          border-radius: 22px !important;
          border:1px solid #dbeaf5 !important;
          background:#fff !important;
          box-shadow:0 16px 45px rgba(21,83,132,.085) !important;
        }
        [data-testid="stForm"] label { color:#183b57 !important; font-weight:600 !important; }
        [data-testid="stForm"] [data-testid="stTextInput"] input {
          background:#f7fbff !important;
          min-height: 45px !important;
          color:#183b57 !important;
        }
        [data-testid="stFormSubmitButton"] button {
          min-height: 48px !important;
          border-radius: 11px !important;
          font-weight:750 !important;
          letter-spacing:.01em !important;
        }
        .stApp::before { opacity: .024 !important; background-position:center 75% !important; }
        @media(max-width:650px) {
          [data-testid="stMainBlockContainer"] {padding:1.35rem 1rem 2rem !important;}
          .nas-brand-hero img {width:min(150px,48vw) !important;max-height:none !important;}
          [data-testid="stForm"] {padding:1.1rem !important;border-radius:17px !important;}
          [data-testid="stMainBlockContainer"] h1 {font-size:1.8rem !important;}
        }
        </style>"""
    # NASAAEM_HIDE_INPUT_HINTS_623
    styles += """
    <style>
      /* Hide Streamlit's keyboard submission instructions. */
      [data-testid="InputInstructions"],
      [data-testid="stInputInstructions"] {
          display: none !important;
      }
    </style>
    """

    # NASAAEM_FINAL_VISUAL_FIX_624
    styles += """
    <style>
    /* Keep the entire original hospital logo visible */
    .nas-brand-hero {
        padding-top: 48px !important;
        margin: 0 auto 8px !important;
        overflow: visible !important;
        position: relative !important;
    }

    .nas-brand-hero img {
        display: block !important;
        width: min(190px, 48vw) !important;
        height: auto !important;
        max-height: none !important;
        object-fit: contain !important;
        object-position: center !important;
        margin: 0 auto !important;
        overflow: visible !important;
    }

    /* Hide Streamlit's keyboard submission instructions */
    [data-testid="InputInstructions"],
    [data-testid="stInputInstructions"],
    div[class*="InputInstructions"],
    [data-testid="stTextInput"] [data-testid*="Instruction"] {
        display: none !important;
    }

    /* Keep form fields clean and readable */
    [data-testid="stTextInput"] input {
        padding-right: 14px !important;
    }
    </style>
    """

    # NASAAEM_FIX_626: Preserve full logo and hide any legacy keyboard hints.
    styles += """<style>
      .nas-brand-hero { overflow: visible !important; padding: 0 !important; }
      .nas-brand-hero img {
        display: block !important;
        width: min(255px, 67vw) !important;
        height: auto !important;
        max-height: none !important;
        object-fit: contain !important;
        margin: 0 auto !important;
      }
      div[data-testid="InputInstructions"],
      div[data-testid="InputInstructions"] span,
      [data-testid="stInputInstructions"] { display:none !important; }
    </style>"""
    # NASAAEM_TRANSPARENT_LOGO_AND_HINTS_628
    styles += """<style>
      /* Streamlit form input hint: hide text, not the actual input or its label. */
      div[data-testid="InputInstructions"],
      div[data-testid="InputInstructions"] > span:first-child,
      [data-testid="stInputInstructions"],
      [data-testid*="inputinstructions" i],
      [class*="inputinstructions" i],
      [class*="InputInstructions"] {
          display: none !important;
          visibility: hidden !important;
          opacity: 0 !important;
      }
      /* Preserve full original transparent logo, never clip it. */
      .nas-brand-hero, .nas-brand-hero img {
          overflow: visible !important;
          clip-path: none !important;
      }
      .nas-brand-hero img {
          height: auto !important;
          max-height: none !important;
          object-fit: contain !important;
      }
    </style>"""

    # NASAAEM_REFINED_UI_632
    styles += """
    <style>
    /* Remove the instruction container beside text inputs */
    [data-testid="stForm"]
    [data-testid="stTextInputRootElement"]
    input[data-testid="stTextInputField"] + div {
        display: none !important;
    }

    /* More visible, centrally positioned hospital watermark */
    .stApp::before {
        opacity: 0.065 !important;
        background-position: center 54% !important;
        background-size: min(58vw, 620px) auto !important;
    }

    @media (max-width: 650px) {
        .stApp::before {
            opacity: 0.05 !important;
            background-size: 85vw auto !important;
        }
    }
    </style>
    """

    # NASAAEM_STYLESHEET_REPAIR_647
    import re

    css_blocks = re.findall(
        r"(?is)<style[^>]*>(.*?)</style\s*>",
        styles,
    )

    if not css_blocks:
        raise RuntimeError("No hospital CSS blocks found.")

    clean_styles = "<style>\n" + "\n".join(css_blocks) + "\n</style>"
    st.html(clean_styles)

    if is_login:
        st.markdown(
            '<div class="nas-brand-hero">'
            + (f'<img src="{data_uri}" alt="Nasaaem Hospital logo">' if data_uri else '')
            + '<div class="nas-brand-caption">NASAAEM HOSPITAL</div>'
            + '<div class="nas-brand-rule"></div></div>',
            unsafe_allow_html=True,
        )
    else:
        pass
