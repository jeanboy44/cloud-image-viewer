import os
import yaml
from pathlib import Path
from copy import deepcopy
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid
from st_aggrid.shared import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from utils import Connector, ConfigHandler, FileSystem

PATH = "kfood/튀김/"
BLOB = "kfood/튀김/오징어튀김/Img_142_0007.jpg"
# st.session_state["repo_type"] = "local"

# class ConfigHandler:
#     def __init__(self):
#         self.config = None

#     def read_config(self, file="config.yml"):
#         with open(file, mode="r"):
#             self.config = yaml.load(file, Loader=yaml.FullLoader)

# ---------------------------------------------------------------

# @st.cache
# def initialize():
#     ch = ConfigHandler()
#     conn = Connector()
#     conn.connection_info = ch.config["accounts"]["azure_jgryu"]
#     conn.connect()

#     return conn

# st.secrets["azure"]


@st.cache
def load_blob_list(conn, path=PATH, type="local"):
    if type == "cloud":
        path_list, isdir_list = conn.get_list(path)
        df = pd.DataFrame({"path": path_list, "is_dir": isdir_list})
    elif type == "local":
        fs = FileSystem()
        path_list, isdir_list = fs.get_list(path)
        df = pd.DataFrame({"path": path_list, "is_dir": isdir_list})

    return df


@st.cache(
    allow_output_mutation=True,
    hash_funcs={"_thread.RLock": lambda _: None, "builtins.weakref": lambda _: None},
)
def init_connection():
    conn = Connector()
    conn.connect(st.secrets["azure"])
    return conn


@st.cache
def read_image(conn, path, type):
    if type == "cloud":
        blob_client = conn.connector.get_blob_client(path)
        byte = blob_client.download_blob().content_as_bytes()

    if type == "local":
        with open(path, "rb") as f:
            byte = f.read()

    return byte


def download_image(conn, src, dest_dir):
    dest_ = os.path.join(dest_dir, Path(src).name)
    conn.download(src, dest_)


st.set_page_config(layout="wide")
st.title("Cloud Image Viewer")

# Initialize state.
if "current_image_path" not in st.session_state:
    st.session_state.current_image_path = ""
    st.session_state.current_dir = ""

conn = init_connection()

add_selectbox = st.sidebar.selectbox(
    "Repository Type", ("local", "cloud"), key="repo_type"
)
add_textinput = st.sidebar.text_input(label="Download dir", key="download_dir")


col1, col2 = st.columns([0.9, 0.1])
with col1:
    st.text_input(label="Current dir", value="kfood/", key="current_dir")
    # st.text_input("Enter blob path", key="root_dir", on_change=load_blob_list)
    df = load_blob_list(
        conn, path=st.session_state.current_dir, type=st.session_state.repo_type
    )
    gb = GridOptionsBuilder.from_dataframe(df)
    # df_dir = df.loc[df.is_dir ==True]
    # df_path = df.loc[df.is_dir ==False]
    gb.configure_selection(selection_mode="single")
    # gb.configure_pagination(enabled=True, paginationPageSize=5, )
    gridOptions = gb.build()
with col2:
    st.button(
        label="Download",
        key="download",
        on_click=download_image,
        args=(conn, st.session_state.current_image_path, st.session_state.download_dir),
    )

# with col1:
data = AgGrid(
    df,
    height=200,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    allow_unsafe_jscode=True,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
)
try:
    data_selected = data["selected_rows"][0]
    path = data_selected["path"]
    is_dir = data_selected["is_dir"]
except:
    path = ""
    is_dir = False
st.session_state.current_image_path = path

# with col2:
try:
    contents = read_image(
        conn, st.session_state.current_image_path, type=st.session_state.repo_type
    )
    st.image(contents)
except:
    st.empty()
