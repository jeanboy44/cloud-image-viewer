import streamlit as st
import pandas as pd

from st_aggrid import AgGrid
from st_aggrid.shared import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Initialize session states
if "filtered_data" not in st.session_state:
    st.session_state.filtered_data = None

# Functions
@st.cache
def read_image(path):
    with open(path, "rb") as f:
        byte = f.read()

    return byte


def main():
    st.sidebar.write("-----")
    show_label = st.sidebar.checkbox(label="show_annotation")
    if show_label:
        form = st.sidebar.form("aonnotation_dir")
        form.text_input(label="annotation_dir", key="annotation_dir")
        form.form_submit_button("Apply")
    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        st.markdown("### File list")
        gb = GridOptionsBuilder.from_dataframe(st.session_state.filtered_data)
        gb.configure_selection(selection_mode="single")
        gridOptions = gb.build()
        ag_data = AgGrid(
            st.session_state.filtered_data,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            allow_unsafe_jscode=True,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
        )
        try:
            data_selected = ag_data["selected_rows"][0]
            path = data_selected["path"]
        except:
            path = ""
    with col2:
        st.markdown("### Image")
        try:
            img = read_image(path)
            st.image(img)
        except:
            st.empty()
        st.write(path)


if __name__ == "__main__":
    main()
