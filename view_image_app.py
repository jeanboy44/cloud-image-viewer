import streamlit as st
import pandas as pd

import cv2
import numpy as np

from pathlib import Path
import imgaug as ia
from PIL import Image
from st_aggrid import AgGrid
from st_aggrid.shared import JsCode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from utils import PascalVocReader


# cellsytle_jscode = JsCode(
#     """
# function(params) {
#     if (params.value.includes(False)) {
#         return {
#             'color': 'white',
#             'backgroundColor': 'darkred'
#         }
#     } else {
#         return {
#             'color': 'black',
#             'backgroundColor': 'white'
#         }
#     }
# };
# """
# )

# Functions
@st.cache
def read_image(path, annotation=False):

    # with open(path, "rb") as f:
    #     byte = Image
    image = Image.open(path)

    if annotation is True:
        try:
            file_path = str(
                Path(st.session_state.annotation_dir).joinpath(f"{Path(path).stem}.xml")
            )
            reader = PascalVocReader(file_path)
            reader.parse_xml()
            # encoded_img = np.fromstring(byte, dtype=np.uint8)
            # image = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
            image = np.asarray(image)
            bbs = ia.BoundingBoxesOnImage(reader.boxes, shape=image.shape)
            image = bbs.draw_on_image(image)
        except:
            pass

    return image


def load_labels():
    """"""
    annots = [f.stem for f in Path(st.session_state.annotation_dir).glob("*.xml")]
    # reader = PascalVocReader(file_path)
    # reader.parse_xml()
    return pd.DataFrame({"file": annots, "annotation": True})


def main():
    st.sidebar.write("-----")
    co1, col2 = st.sidebar.columns(2)
    show_annot = co1.checkbox(label="show_annotation")
    data = st.session_state.filtered_data[["file", "path"]]
    if show_annot:
        show_only_annot = col2.checkbox(label="only")
        st.sidebar.text_input(
            label="annotation_dir", key="annotation_dir", on_change=load_labels
        )
        data_label = load_labels()
        if data_label.shape[0] == 0:
            st.sidebar.warning(f"{data_label.shape[0]} annotations loaded")
        else:
            st.sidebar.success(f"{data_label.shape[0]} annotations loaded")

        if show_only_annot:
            data = pd.merge(data, data_label, how="inner")
            data = data.fillna(False)
        else:
            data = pd.merge(data, data_label, how="left")
            data = data.fillna(False)

    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        st.markdown("### File list")
        gb = GridOptionsBuilder.from_dataframe(data)
        gb.configure_selection(selection_mode="single")
        gridOptions = gb.build()
        ag_data = AgGrid(
            data,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            allow_unsafe_jscode=True,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
        )
        try:
            if "current_path" not in st.session_state:
                st.session_state.current_path = data["path"][0]
            else:
                data_selected = ag_data["selected_rows"][0]
                path = data_selected["path"]
                st.session_state.current_path = path
        except:
            path = None
    with col2:
        st.markdown("### Image")
        try:
            img = read_image(st.session_state.current_path, annotation=show_annot)
            st.image(img)
        except Exception as e:
            st.empty()
            st.error(e)
        st.write(st.session_state.current_path)


if __name__ == "__main__":
    main()
