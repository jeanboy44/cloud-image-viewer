import streamlit as st
import pandas as pd

from st_aggrid import AgGrid
from st_aggrid.shared import JsCode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from utils import load_image, load_labels

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


def annotation_dir_changed():
    st.session_state.annotation_dir_ = st.session_state.annotation_dir


def show_annot_clicked():
    st.session_state.show_annot_ = st.session_state.show_annot


def show_annot_only_clicked():
    st.session_state.show_annot_only_ = st.session_state.show_annot_only


def main():
    st.sidebar.write("-----")
    st.sidebar.write("Image Configurations")
    form = st.sidebar.form(key="image_configuration")
    form.number_input(
        label="Scale",
        min_value=0.1,
        max_value=1.0,
        value=0.3,
        step=0.1,
        key="image_scale",
    )
    form.form_submit_button("Apply")

    co1, col2 = st.sidebar.columns(2)
    show_annot = co1.checkbox(
        label="show_annotation", key="show_annot", on_change=show_annot_clicked
    )
    data = st.session_state.filtered_data[["file", "path"]]
    if show_annot:
        show_only_annot = col2.checkbox(
            label="only", key="show_annot_only", on_change=show_annot_only_clicked
        )
        st.sidebar.text_input(
            label="annotation_dir",
            key="annotation_dir",
            on_change=annotation_dir_changed,
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
        if "current_path" not in st.session_state:
            try:
                st.session_state.current_path = data["path"][0]
            except:
                st.session_state.current_path = ""

        try:
            data_selected = ag_data["selected_rows"][0]
            path = data_selected["path"]
            st.session_state.current_path = path
        except:
            path = None
    with col2:
        st.markdown("### Image")
        try:
            img, error_msg = load_image(
                st.session_state.current_path,
                resize_ratio=st.session_state.image_scale,
                annotation=st.session_state.show_annot,
                annotation_dir=st.session_state.annotation_dir,
            )
            st.image(img)
            if error_msg is not None:
                st.error(error_msg)
        except Exception as e:
            st.empty()
            st.error(e)
        st.write(st.session_state.current_path)


if __name__ == "__main__":
    main()
