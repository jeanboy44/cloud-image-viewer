import yaml
import streamlit as st

from utils import connect

CONFIG_FILE = "config.yml"


def repo_on_change():
    st.session_state.repo_ = st.session_state.repo


def main():

    col1, col2, col3 = st.columns(3)
    col1.selectbox(
        "Repository",
        options=("Local", "AzureTest", "AWSTest"),
        key="repo",
        on_change=repo_on_change,
    )

    if st.session_state.repo == "Local":
        st.session_state.repo_condition = "Local ✅"
    else:
        try:
            connect(st.session_state.repo)
            st.session_state.repo_condition = f"{st.session_state.repo} ✅"
            st.session_state.root_dir = ""
            st.session_state.root_dir_ = ""
            st.session_state.show_annot = False
            st.session_state.show_annot_ = False
            st.session_state.show_annot_only = False
            st.session_state.show_annot_only_ = False
            st.session_state.annotation_dir = ""
            st.session_state.annotation_dir_ = ""
            # st.session_state.loaded_data = None
            # st.session_state.filtered_data = None
            col1.success("Connection Successed!")
        except:
            st.session_state.repo_condition = f"{st.session_state.repo} 🚫"
            col1.error("Connection Failed!")


if __name__ == "__main__":
    main()
