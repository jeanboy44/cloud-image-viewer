import yaml
from copy import deepcopy
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid
from st_aggrid.shared import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from utils import Connector, ConfigHandler

PATH = "kfood/튀김/오징어튀김/"
BLOB = "kfood/튀김/오징어튀김/Img_142_0007.jpg"


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


def load_blob_list(conn, path=PATH):
    path_list, isdir_list = conn.get_list(path)
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
def read_image(conn, blob):
    blob_client = conn.connector.get_blob_client(blob)
    byte = blob_client.download_blob().content_as_bytes()
    return byte


st.set_page_config(layout="wide")
st.title("Cloud Image Viewer")

st.session_state.current_image_path = ""

conn = init_connection()
col1, col2 = st.columns([1, 5])
# st.text_input("Enter blob path", key="root_dir", on_change=load_blob_list)
df = load_blob_list(conn)
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection(selection_mode="single")
# gb.configure_pagination()
gridOptions = gb.build()

with col1:
    data = AgGrid(
        df,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
    )
    st.session_state.current_image_path = data["selected_rows"][0]["path"]

with col2:
    print(st.session_state.current_image_path)
    contents = read_image(conn, st.session_state.current_image_path)
    st.image(contents)
