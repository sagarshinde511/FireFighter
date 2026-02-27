import streamlit as st
from ftplib import FTP
import urllib.parse

# ---------------- CONFIGURATION ----------------
FTP_HOST = "82.180.143.66"
FTP_USER = "u263681140"
FTP_PASS = "SagarA@2025"
REMOTE_PATH = "FireFighter"
BASE_WEB_URL = "http://aeprojecthub.in/FireFighter/"

ADMIN_USER = "admin"
ADMIN_PASS = "admin"
# -----------------------------------------------

st.set_page_config(page_title="FireFighter Video Gallery", layout="wide")

# Login State Management
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔒 FireFighter Login")
    with st.form("login"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if u == ADMIN_USER and p == ADMIN_PASS:
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Access Denied")
    st.stop()

# --- APP CONTENT ---

@st.cache_data(ttl=300)
def get_video_list():
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(REMOTE_PATH)
        files = ftp.nlst()
        ftp.quit()
        # Filter and sort (Newest files usually have higher numeric/alphabetical names)
        return sorted([f for f in files if f.endswith('.mp4')], reverse=True)
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return []

st.title("🔥 FireFighter Video Monitor")

videos = get_video_list()

if not videos:
    st.warning("No MP4 files found on the server.")
else:
    # Sidebar for Video Selection
    st.sidebar.title("Navigation")
    selected_video = st.sidebar.radio("Select Recording:", videos)
    
    if st.sidebar.button("🔄 Refresh List"):
        st.cache_data.clear()
        st.rerun()

    if st.sidebar.button("🚪 Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

    # --- MAIN DISPLAY ---
    st.subheader(f"Viewing: {selected_video}")
    
    # URL Encoding handles spaces or special characters in filenames
    encoded_name = urllib.parse.quote(selected_video)
    full_url = f"{BASE_WEB_URL}{encoded_name}"
    
    # The 'st.video' component provides full-screen, volume, and download options
    st.video(full_url, format="video/mp4", start_time=0)
    
    st.info(f"Direct Link: {full_url}")

    # Optional: Display Gallery Grid below
    st.divider()
    st.subheader("Recent Captures")
    cols = st.columns(4)
    for i, vid in enumerate(videos[:8]):
        with cols[i % 4]:
            st.caption(vid)
            # Small preview player
            st.video(f"{BASE_WEB_URL}{urllib.parse.quote(vid)}")
