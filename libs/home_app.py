import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.shared import GridUpdateMode

import pandas as pd

from .utils import load_data, SessionStateHandler as ss

# Load data and images
@st.cache
def get_filter_info(data):
    # load data
    df = data.copy()
    df = df.dir.str.split(pat="/", n=100, expand=True)
    df = df.drop_duplicates()
    df.columns = [f"level_{col}" for col in df.columns]

    return df


def load_filter(data):
    filter_list = {}
    for col in data.columns:
        ss.initialize_session_state(
            col, data[col].dropna().unique().tolist(), slider=True
        )
        filter_list[col] = data[col].dropna().unique().tolist()

    return filter_list


# @st.cache
def filter_data(data, filter_info):
    cond = [True for i in range(filter_info.shape[0])]
    for col in filter_info.columns:
        new_cond = (
            pd.Series(filter_info[col]).isin(st.session_state[col])
            | pd.Series(filter_info[col]).isna()
        )
        for i, (c_, nc_) in enumerate(zip(cond, new_cond)):
            cond[i] = c_ & nc_

    filter_info = filter_info[cond]
    dir_filter = filter_info.apply(
        lambda row: "/".join(row.dropna().values.astype(str)), axis=1
    )
    return data[data.dir.isin(dir_filter)]


def main():
    """"""
    st.sidebar.write("----")
    st.sidebar.text_input(
        label="root_dir", key="root_dir", on_change=ss.root_dir_entered
    )

    loaded_data = load_data(st.session_state.root_dir, st.session_state.connector)
    filter_info = get_filter_info(loaded_data)
    filters_ = load_filter(filter_info)

    st.session_state.filtered_data = filter_data(
        data=loaded_data, filter_info=filter_info
    )
    col1, col2, col3 = st.columns([0.2, 0.4, 0.4])
    with col1:
        st.markdown("### File list")
        # st.sidebar.
        ag_data = AgGrid(
            pd.DataFrame(st.session_state.filtered_data["path"]),
            enable_enterprise_modules=True,
            allow_unsafe_jscode=True,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
        )

    with col2:
        st.markdown("### Filter form")
        for name, values in filters_.items():
            st.multiselect(
                label=name,
                options=values,
                on_change=ss.level_selected,
                key=name,
            )


if __name__ == "__main__":
    main()
