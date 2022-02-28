from lib2to3.pgen2.pgen import DFAState
import streamlit as st
import pandas as pd
from pathlib import Path

from st_aggrid import AgGrid
from st_aggrid.shared import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder


@st.cache
def load_data():
    # load data
    paths = []
    for path in Path("/Users/jeanboy/Dropbox/Temporary").rglob("*.jpg"):
        paths.append(str(path))

    # parse data
    df = pd.DataFrame({"path": paths})
    df["dir"] = [str(Path(path).parent) for path in df.path]
    return df


@st.cache
def get_filter_info(data):
    # load data
    df = data.copy()
    df = df.dir.str.split(pat="/", n=100, expand=True)
    df = df.drop_duplicates()
    df.columns = [f"level_{col}" for col in df.columns]

    return df


def handle_change():
    for key in st.session_state.keys():
        if key[:5] == "level":
            st.session_state[key[:-12]] = st.session_state[f"{key}"]


def load_filter(data):
    filter_list = {}
    for col in data.columns:
        if col not in st.session_state:
            if f"{col}_multiselect" in st.session_state:
                st.session_state[col] = st.session_state[f"{col}_multiselect"]
            else:
                st.session_state[col] = data[col].dropna().unique().tolist()
                st.session_state[f"{col}_multiselect"] = (
                    data[col].dropna().unique().tolist()
                )
        else:
            if f"{col}_multiselect" not in st.session_state:
                st.session_state[f"{col}_multiselect"] = st.session_state[col]

        filter_list[col] = data[col].dropna().unique().tolist()
        # else:
        #     filter_list[col] = st.session_state[col]

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
    loaded_data = load_data()
    filter_info = get_filter_info(loaded_data)
    filters_ = load_filter(filter_info)

    st.session_state.filtered_data = filter_data(
        data=loaded_data, filter_info=filter_info
    )

    col1, col2, col3 = st.columns([0.2, 0.4, 0.4])
    with col1:
        st.markdown("### File list")
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
                on_change=handle_change,
                key=f"{name}_multiselect",
            )

    with col3:
        st.markdown("### &nbsp;")
        st.text_input("Level 3", key="t3")
        st.text_input("Level 4", key="t4")
        st.number_input("Max number2")


if __name__ == "__main__":
    main()
