import streamlit as st
from ftplib import FTP
import pandas as pd

# ---------------- CONFIGURATION ----------------
FTP_HOST = "82.180.143.66"
FTP_USER = "u263681140"
FTP_PASS = "SagarA@2025"
REMOTE_PATH = "FireFighter"
BASE_WEB_URL = "http://aeprojecthub.in/FireFighter/"
# -----------------------------------------------

st.set_page_config(page_title="FireFighter Video Gallery", layout="wide")

st.title("🔥 FireFighter: Cloud Video Gallery")
st.markdown(f"Accessing recordings from: `{BASE_WEB_URL}`")

def get_video_list():
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(REMOTE_PATH)
        
        # Get all filenames in the folder
        files = ftp.nlst()
        ftp.quit()
        
        # Filter only mp4 files and sort by newest first
        video_files = [f for f in files if f.endswith('.mp4')]
        video_files.sort(reverse=True)
        return video_files
    except Exception as e:
        st.error(f"Error connecting to FTP: {e}")
        return []

# Sidebar for controls
if st.sidebar.button("🔄 Refresh Gallery"):
    st.cache_data.clear()

videos = get_video_list()

if not videos:
    st.info("No videos found in the FireFighter folder.")
else:
    st.sidebar.write(f"Total Videos: {len(videos)}")
    
    # Selection box to pick a video
    selected_video = st.selectbox("Select a video to play:", videos)
    
    # Layout: Top video player
    st.subheader(f"Playing: {selected_video}")
    video_url = BASE_WEB_URL + selected_video
    st.video(video_url)
    
    st.divider()
    
    # Bottom Layout: Grid gallery
    st.subheader("Recent Uploads")
    cols = st.columns(3)
    for i, vid in enumerate(videos[:9]): # Show top 9 in grid
        with cols[i % 3]:
            st.write(f"📄 {vid}")
            # Smaller player for the grid
            st.video(BASE_WEB_URL + vid)
