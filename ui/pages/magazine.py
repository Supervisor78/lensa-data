import streamlit as st
from logic.data_processing import get_sales_data, process_magazine
from ui.translations import get_translation
from ui.components.charts import show_bar_chart, show_map
import logging


def run(oct_start, nov_end, include_bonuses):
    st.title(get_translation("page_magazine"))

    logging.debug(f"Fetching sales data from {oct_start} to {nov_end} with include_bonuses={include_bonuses}")

    df_sales = get_sales_data(oct_start, nov_end)

    if df_sales.empty:
        st.warning(get_translation("no_data"))
        return

    df_magazine = process_magazine(df_sales, include_bonuses)
    if df_magazine.empty:
        st.warning(get_translation("no_data"))
        return

    st.dataframe(df_magazine[['Magazin', 'Vanzari', 'Target', 'Procent din target']])

    # Adauga optiunea de a alege intre Bar chart si Map
    visualization_type = st.radio(
        "Select visualization type",
        ["Bar chart", "Map"],
        index=0  # Default este bar chart
    )

    if visualization_type == "Bar chart":
        show_bar_chart(df_magazine, x_col='Magazin', y_col='Procent din target', title=get_translation("stores_chart"))
    elif visualization_type == "Map":
        show_map(df_magazine, column='Procent din target', title=get_translation("stores_map"))

    # Explicație
    st.markdown("### Explanation")
    st.write("This visualization shows the percentage of target achieved by each store.")
