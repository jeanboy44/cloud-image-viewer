import yaml
import streamlit as st

from utils import load_data, SessionStateHandler as ss

CONFIG_FILE = "config.yml"


def main():
    col1, col2, col3 = st.columns(3)
    col1.selectbox(
        "Repository",
        options=[key for key in st.secrets.keys()],
        key="repo",
        on_change=ss.repo_on_change,
    )

    # if st.session_state.connection_name == "Local":

    #     st.session_state.repo_condition = "Local ✅"
    # else:
    try:
        connector_ = st.session_state.connector
        connector_.connect(name=st.session_state.repo)
        st.session_state.connector = connector_

        st.session_state.root_dir = connector_.default_dir
        st.session_state.root_dir_ = connector_.default_dir
        ss.root_dir_entered()
        st.session_state.show_annot = False
        st.session_state.show_annot_ = False
        st.session_state.show_annot_only = False
        st.session_state.show_annot_only_ = False
        st.session_state.annotation_dir = ""
        st.session_state.annotation_dir_ = ""
        col1.success("Connection Successed!")
    except Exception as e:
        st.write("-------")
        col1.error("Connection Failed!")
        col1.error(e)


if __name__ == "__main__":
    main()
