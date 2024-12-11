import streamlit as st
import logging

from logic.data_processing import get_latest_year_with_data_for_oct_nov
from ui.translations import get_translation
import ui.pages.categorii
import ui.pages.magazine

# Set page config
st.set_page_config(page_title=get_translation("title"), layout="wide")

# Sidebar
st.sidebar.title(get_translation("filters_title"))
include_bonuses = st.sidebar.checkbox(get_translation("include_bonuses"), value=True)

page = st.sidebar.radio(
    get_translation("select_page"),
    [get_translation("page_categorii"), get_translation("page_magazine")]
)

# Ensure that the year and date range are correct
def run_app():
    # Fetch the latest year for October-November
    year = get_latest_year_with_data_for_oct_nov()
    if year is None:
        st.warning("Nu s-au găsit date pentru octombrie-noiembrie în niciun an.")
        return

    # Set date range for October-November
    oct_start = f"{year}-10-01"
    nov_end = f"{year}-11-30"

    # Log the used date range for debugging
    logging.debug(f"Using the date range: {oct_start} to {nov_end} for the year {year}")

    # Pass the correct date range to the pages
    if page == get_translation("page_categorii"):
        ui.pages.categorii.run(oct_start, nov_end, include_bonuses)
    else:
        ui.pages.magazine.run(oct_start, nov_end, include_bonuses)

run_app()
