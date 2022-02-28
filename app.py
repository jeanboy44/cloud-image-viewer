# Core Pkgs
import streamlit as st

# Additional Pkgs
import pandas as pd

# Import File/Data

# More Fxn
from utils import connect
from home_app import main as home
from view_image_app import main as view_image

# Initialize session states
if "connection_type" not in st.session_state:
    st.session_state.connection_type = None
    st.session_state.connector = None

# Config Page
PAGE_CONFIG = {
    "page_title": "CloudImageViewer",
    "page_icon": "🐰",
    "layout": "wide",
}
st.set_page_config(**PAGE_CONFIG)
st.session_state.connector = connect()


def main():
    menu = ["Filter", "View Images", "Settings", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    st.title("Cloud Image Viewer")
    if choice == "Filter":
        home()
    elif choice == "View Images":
        view_image()
    elif choice == "Settings":
        st.subheader("Settings")
    else:
        st.subheader("About")


if __name__ == "__main__":
    main()
