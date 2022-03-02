import yaml
import streamlit as st

from utils import connect

CONFIG_FILE = "config.yml"


def main():

    col1, col2, col3 = st.columns(3)
    col1.selectbox("Repository", options=("Local", "AzureTest", "AWSTest"), key="repo")

    if st.session_state.repo != "Local":
        try:
            connect(st.session_state.repo)
            st.session_state.repo_condition = f"{st.session_state.repo} ✅"
            col1.success("Connection Successed!")
        except:
            st.session_state.repo_condition = f"{st.session_state.repo} 🚫"
            col1.error("Connection Failed!")


if __name__ == "__main__":
    main()
