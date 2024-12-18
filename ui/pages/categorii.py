import streamlit as st
import logging
from logic.data_processing import get_sales_data, process_categorii
from ui.translations import get_translation
from ui.components.filters import get_oct_nov_dates
from ui.components.charts import show_bar_chart, show_pie_chart


def run(oct_start, nov_end, include_bonuses):
    st.title(get_translation("page_categorii"))

    # asigura ca intervalul de date este corect
    logging.debug(f"Fetching sales data from {oct_start} to {nov_end} with include_bonuses={include_bonuses}")

    df_sales = get_sales_data(oct_start, nov_end)

    if df_sales.empty:
        st.warning(get_translation("no_data"))
        return

    df_categorii = process_categorii(df_sales, include_bonuses)
    if df_categorii.empty:
        st.warning(get_translation("no_data"))
        return

    st.dataframe(df_categorii[['Categorie', 'Vanzari', 'Target', 'Procent din target']])

    # adauga optiunea de a alege intre Bar chart si Pie chart
    chart_type = st.radio(
        "Selecteaza tipul de vizualizare",
        ["Bar chart", "Pie chart"],
        index=0  # Default este bar chart
    )

    if chart_type == "Bar chart":
        show_bar_chart(df_categorii, x_col='Categorie', y_col='Procent din target', title=get_translation("categories_chart"))
    else:
        show_pie_chart(df_categorii, column='Procent din target', title=get_translation("Categorii"))
