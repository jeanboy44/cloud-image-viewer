import streamlit as st
import pandas as pd

from st_aggrid import AgGrid
from st_aggrid.shared import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder


def main():
    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        df = pd.read_csv("resources/iris.csv")
        df = pd.DataFrame(df["species"])

        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_selection(selection_mode="single")
        gridOptions = gb.build()
        data = AgGrid(
            df,
            height=200,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            allow_unsafe_jscode=True,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
        )
    with col2:
        st.image("resources/image_01.jpeg")


if __name__ == "__main__":
    main()
