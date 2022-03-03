# Core Pkgs
import streamlit as st

# Additional Pkgs
import pandas as pd

# Import File/Data

# More Fxn
from utils import connect
from home_app import main as home
from view_image_app import main as view_image
from settings_app import main as settings

ROOT_DIR = "sample_images/"

# Initialize session states
if "connection_type" not in st.session_state:
    st.session_state.connection_type = None
    st.session_state.connector = None
    st.session_state.repo = "Local"
    st.session_state.repo_condition = "Local✅"
    st.session_state.annotation_dir = ""

# Initialize session states
if "root_dir_textinput" not in st.session_state:
    if "root_dir" in st.session_state:
        st.session_state.root_dir_textinput = st.session_state.root_dir
    else:
        st.session_state.root_dir = ROOT_DIR
        st.session_state.root_dir_textinput = ROOT_DIR

# Initialize sessionstates
# if "annotation_dir" not in st.session_state:
#     st.session_state.annotation_dir = ""

# Config Page
PAGE_CONFIG = {
    "page_title": "CloudImageViewer",
    "page_icon": "🐰",
    "layout": "wide",
}
st.set_page_config(**PAGE_CONFIG)


def main():
    menu = ["Filter", "View Images", "Settings", "About"]
    container = st.sidebar.container()
    choice = st.sidebar.selectbox("Menu", menu)
    st.title("Cloud Image Viewer")
    if choice == "Filter":
        home()
    elif choice == "View Images":
        view_image()
    elif choice == "Settings":
        st.subheader("Settings")
        settings()
    else:
        st.subheader("About")

    container.text(f"Repo: {st.session_state.repo_condition}")


if __name__ == "__main__":
    main()
