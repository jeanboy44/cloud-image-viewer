# Core Pkgs
import streamlit as st

# Additional Pkgs

# Import File/Data

# More Fxn
from home_app import main as home

# Config Page
PAGE_CONFIG = {
    "page_title": "CloudImageViewer",
    "page_icon": "🐰",
    "layout": "wide",
}
st.set_page_config(**PAGE_CONFIG)


def main():
    menu = ["Home", "Settings", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.title("Cloud Image Viewer")
        home()
    elif choice == "Settings":
        st.title("Settings")
    else:
        st.title("About")


if __name__ == "__main__":
    main()
