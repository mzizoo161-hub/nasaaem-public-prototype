"""Unified Nasaaem styling and navigation for authenticated prototype pages."""
from pathlib import Path
from html import escape
import base64
import streamlit as st


def _logo_data_uri():
    file = Path(__file__).resolve().parent / 'assets' / 'nasaaem_hospital_logo.png'
    if not file.is_file():
        return ''
    return 'data:image/png;base64,' + base64.b64encode(file.read_bytes()).decode('ascii')


def apply_workspace_theme():
    """Workspace only: the existing login layout remains untouched."""
    watermark = _logo_data_uri()
    css = r"""
    <style>
    :root {--hospital-navy:#0c4478;--hospital-blue:#1467a5;--hospital-sky:#5db7e1;
      --hospital-ink:#16395b;--hospital-muted:#5f7790;--hospital-line:#dce8f4;}
    /* The logo watermark stays behind all interactive content. */
    .stApp {background:linear-gradient(135deg,#f5faff 0%,#edf5ff 52%,#f9fcff 100%) !important;}
    .stApp::before {
       background-image:url('NASAAEM_WORKSPACE_LOGO') !important;
       background-repeat:no-repeat !important;
       background-position:62% 58% !important;
       background-size:min(56vw,680px) auto !important;
       opacity:.055 !important;pointer-events:none !important;
    }
    [data-testid="stMainBlockContainer"] {
        max-width:1420px !important;padding:1.25rem 1.9rem 3rem !important;
    }
    section[data-testid="stSidebar"] {background:linear-gradient(180deg,#0d4f88,#0b3868) !important;
       border-right:1px solid rgba(255,255,255,.1) !important;}
    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {padding-top:1.1rem !important;}
    section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] small {color:#f4f9ff !important;}
    section[data-testid="stSidebar"] div[data-testid="stButton"] button {
       width:100%;justify-content:flex-start;text-align:left;
       border-radius:11px !important;min-height:2.85rem !important;
       border:1px solid rgba(255,255,255,.12) !important;
       color:#f6fbff !important;background:rgba(255,255,255,.07) !important;
       font-weight:600 !important;box-shadow:none !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover,
    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"] {
       background:rgba(255,255,255,.22) !important;border-color:rgba(255,255,255,.48) !important;
    }
    .nas-side-brand {text-align:center;padding:.2rem .2rem 1rem;border-bottom:1px solid rgba(255,255,255,.18);
       margin-bottom:1rem;}
    .nas-side-brand img {width:min(180px,90%);max-height:125px;object-fit:contain;display:block;margin:0 auto .65rem;}
    .nas-side-brand strong {display:block;color:#fff;font-size:1.06rem;letter-spacing:-.02em;}
    .nas-side-brand span {display:block;color:#cde5fb;font-size:.72rem;margin-top:.3rem;}
    .nas-side-profile {background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.17);
       padding:.8rem .85rem;border-radius:13px;color:#fff;font-size:.85rem;margin:.9rem 0;}
    .nas-side-profile strong {color:#fff;display:block;overflow-wrap:anywhere;}
    .nas-side-profile small {color:#d1e7fa;display:block;margin-top:.2rem;}
    .nas-hero {position:relative;overflow:hidden;border-radius:21px;padding:1.6rem 1.85rem;
       margin:.35rem 0 1.15rem;border:1px solid #d9e8f6;
       background:linear-gradient(100deg,rgba(255,255,255,.97),rgba(218,238,255,.82));
       box-shadow:0 10px 30px rgba(20,75,115,.06);}
    .nas-hero:after {content:'';position:absolute;width:220px;height:220px;border-radius:50%;
       background:rgba(52,151,211,.07);right:-45px;top:-105px;pointer-events:none;}
    .nas-kicker {font-size:.75rem;letter-spacing:.13em;text-transform:uppercase;
       color:#267ba8;font-weight:760;margin:0 0 .4rem;}
    .nas-hero h2 {font-size:clamp(1.5rem,2.7vw,2.2rem) !important;color:#0f477c !important;
       line-height:1.2;margin:0 0 .4rem !important;letter-spacing:-.025em;}
    .nas-hero p {color:#54718d;margin:0;font-size:1rem;}
    /* Consistent containers for all role dashboards and ticket pages. */
    [data-testid="stVerticalBlockBorderWrapper"]:has(>div[data-testid="stVerticalBlock"]) {
       border-radius:17px !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {min-width:0;}
    [data-testid="stMetric"] {background:rgba(255,255,255,.96) !important;
       border:1px solid #dce8f4 !important;border-radius:17px !important;
       box-shadow:0 7px 25px rgba(17,75,121,.045) !important;}
    [data-testid="stForm"] {background:rgba(255,255,255,.97) !important;border:1px solid #dbe8f3 !important;
       box-shadow:0 10px 28px rgba(16,72,112,.07) !important;border-radius:18px !important;}
    [data-testid="stDataFrame"] {border:1px solid #dce7f3 !important;border-radius:14px !important;}
    [data-testid="stTabs"] button {font-weight:650 !important;}
    [data-testid="stExpander"] {border:1px solid #dce8f4 !important;border-radius:14px !important;
       background:rgba(255,255,255,.92) !important;}
    .stButton button,.stDownloadButton button {border-radius:11px !important;min-height:2.8rem !important;}
    .stButton button[kind="primary"],.stDownloadButton button[kind="primary"] {
       background:linear-gradient(115deg,#1677b3,#0f518a) !important;color:#fff !important;
       border-color:#176ca9 !important;}
    h1,h2,h3 {color:#0f477b !important;letter-spacing:-.018em;}
    [data-testid="stAlert"] {border-radius:13px !important;}
    @media(max-width:850px) {
       [data-testid="stMainBlockContainer"] {padding:1rem .85rem 2.3rem !important;}
       .nas-hero {padding:1.15rem 1.1rem;border-radius:16px;}
       .nas-hero p {font-size:.9rem;}
       .stApp::before {background-size:88vw auto !important;background-position:center 70% !important;opacity:.035 !important;}
    }
    </style>
    """
    st.markdown(css.replace('NASAAEM_WORKSPACE_LOGO', watermark), unsafe_allow_html=True)


def render_workspace_navigation(user, is_admin, can_use_dashboard, navigate):
    """Menu links only to pages authorized by the existing portal."""
    with st.sidebar:
        uri = _logo_data_uri()
        image = '<img src="' + uri + '" alt="Nasaaem Hospital" />' if uri else ''
        st.markdown('<div class="nas-side-brand">' + image +
                    '<strong>AI Nasaaem Helpdesk</strong><span>HOSPITAL SUPPORT PORTAL</span></div>',
                    unsafe_allow_html=True)
        name = escape(str(user.get('full_name') or 'Team member'))
        role = escape(str(user.get('role') or 'Employee'))
        department = escape(str(user.get('department') or ''))
        st.markdown('<div class="nas-side-profile"><strong>' + name + '</strong>' +
                    '<small>' + role + ((' · ' + department) if department else '') + '</small></div>',
                    unsafe_allow_html=True)
        choices = [('🏠  Home', 'Home'), ('✍️  New Request', 'Chat'),
                   ('🎫  My Tickets', 'My Tickets')]
        if can_use_dashboard:
            choices.append(('🛠️  Department Tickets', 'Dashboard'))
        if is_admin:
            choices.append(('🛡️  Admin Control Center', 'Admin'))
        current = st.session_state.get('main_page', 'Home')
        for label, target in choices:
            if st.button(label, key='nas_nav_' + target.replace(' ', '_'),
                         use_container_width=True,
                         type='primary' if current == target else 'secondary'):
                if current != target:
                    navigate(target)
        st.markdown('<div style="color:#bedaf1;font-size:.7rem;margin-top:1.3rem;">'
                    'Synthetic prototype · No real hospital records</div>', unsafe_allow_html=True)


def render_workspace_intro(page, user):
    first_name = escape(str(user.get('full_name') or 'Team member').split(' ')[0])
    is_staff = user.get('role') == 'Staff'
    lookup = {
       'Home': ('Welcome back, ' + first_name, 'Choose what you need. Your support requests are just a click away.', 'YOUR WORKSPACE'),
       'Chat': ('Create a support request', 'Describe the issue in your own words. We will help route it to the right department.', 'NEW REQUEST'),
       'My Tickets': ('Track your progress', 'See conversations, respond to updates, and confirm resolutions.', 'TICKET TRACKING'),
       'Dashboard': ('Your department at a glance', 'Review requests and keep employees informed.', 'STAFF WORKSPACE' if is_staff else 'DEPARTMENT OPERATIONS'),
       'Admin': ('Everything in one place', 'Manage tickets, employees and exports with confidence.', 'SYSTEM MANAGEMENT'),
    }
    heading, description, kicker = lookup.get(page, ('Helpdesk', 'Hospital support services', 'NASAAEM'))
    st.markdown('<div class="nas-hero"><div class="nas-kicker">' + kicker +
                '</div><h2>' + heading + '</h2><p>' + description + '</p></div>',
                unsafe_allow_html=True)
