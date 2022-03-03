# Core Pkgs
import streamlit as st

# Additional Pkgs
import pandas as pd

# Import File/Data

# More Fxn
from utils import connect, initialize_session_state
from home_app import main as home
from view_image_app import main as view_image
from settings_app import main as settings

ROOT_DIR = "sample_images/"

# Config Page
PAGE_CONFIG = {
    "page_title": "CloudImageViewer",
    "page_icon": "🐰",
    "layout": "wide",
}
st.set_page_config(**PAGE_CONFIG)

# Initialize session states
# initialize_session_state("connection_type", None)
# initialize_session_state("connector", None)
initialize_session_state("repo_condition", "Local✅")
initialize_session_state("loaded_data", None)
initialize_session_state("filtered_data", None)

initialize_session_state("repo", "Local", slider=True)
initialize_session_state("root_dir", ROOT_DIR, slider=True)
initialize_session_state("show_annot", False, slider=True)
initialize_session_state("show_annot_only", False, slider=True)
initialize_session_state("annotation_dir", "", slider=True)
initialize_session_state("annotation_dir", "", slider=True)


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
