import sqlite3
import pandas as pd
import logging
from logic.queries import QUERY_SALES  # Import the query from queries.py
from logic.config import DB_PATH, TARGET_CATEGORII_PATH, TARGET_MAGAZINE_PATH, INCLUDE_BONUSES  # Use config.py for settings

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

#ia anul cel mai recent cu date pentru octombrie-noiembrie dinamic
def get_latest_year_with_data_for_oct_nov():
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT DISTINCT strftime('%Y', completed) AS year
        FROM orders
        WHERE status='completed'
          AND storno_for IS NULL
          AND strftime('%m', completed) IN ('10','11')
    """
    logging.debug(f"Running query to get the latest year for October-November: {query}")
    df_years = pd.read_sql_query(query, conn)
    conn.close()

    if df_years.empty:
        logging.warning("No data found for October-November in any year.")
        return None

    # Logheaza anii pe care i-am primit din interogare
    logging.debug(f"Available years for October-November: {df_years['year'].tolist()}")

    # Converteste coloana 'year' la int si gaseste anul maxim
    df_years['year'] = df_years['year'].astype(int)
    max_year = df_years['year'].max()

    logging.debug(f"Latest available year with data: {max_year}")
    return max_year

# Returneaza un DataFrame cu datele de vanzari
def get_sales_data(oct_start, nov_end):
    logging.debug(f"Fetching sales data from {oct_start} to {nov_end}")
    conn = sqlite3.connect(DB_PATH)
    logging.debug(f"Executing sales query with parameters: {oct_start}, {nov_end}")
    df_sales = pd.read_sql_query(QUERY_SALES, conn, params=[oct_start, nov_end])
    conn.close()

    logging.debug(f"Fetched {len(df_sales)} rows of data.")
    return df_sales

# proceseaza datele pentru categorii si gestioneaza distributia bonusurilor
def process_categorii(df_sales, include_bonuses):
    if df_sales.empty:
        logging.warning("No sales data to process for categories.")
        return pd.DataFrame(columns=['Categorie', 'Vanzari', 'Target', 'Procent din target'])

    df_categorii = df_sales.groupby('category', as_index=False)['total_sales'].sum()

    # gestioneaza distributia bonusurilor
    if "Bonusuri" in df_categorii['category'].values and include_bonuses:
        total_non_bonus = df_categorii.loc[df_categorii['category'] != 'Bonusuri', 'total_sales'].sum()
        total_bonus = df_categorii.loc[df_categorii['category'] == 'Bonusuri', 'total_sales'].sum()
        if total_non_bonus > 0:
            df_categorii_non_bonus = df_categorii[df_categorii['category'] != 'Bonusuri'].copy()
            df_categorii_non_bonus['total_sales'] += (df_categorii_non_bonus['total_sales'] / total_non_bonus) * total_bonus
            df_categorii = df_categorii_non_bonus

    sheet_name = "Target bonusuri incluse" if include_bonuses else "Target bonusuri separat"
    df_target_categorii = pd.read_excel(TARGET_CATEGORII_PATH, sheet_name=sheet_name)

    df_categorii = pd.merge(df_categorii, df_target_categorii, left_on='category', right_on='categorie', how='left')

    if 'target' not in df_categorii.columns:
        df_categorii['target'] = 0
    df_categorii['Procent din target'] = df_categorii.apply(
        lambda row: (row['total_sales'] / row['target'] * 100) if row['target'] != 0 else 0,
        axis=1
    )

    # Renumește coloanele pentru a se potrivi cu ieșirea așteptată
    df_categorii = df_categorii.rename(columns={'total_sales': 'Vanzari', 'target': 'Target', 'category': 'Categorie'})

    logging.debug(f"Processed category data: {df_categorii.head()}")
    return df_categorii




def process_magazine(df_sales, include_bonuses):
    if df_sales.empty:
        logging.warning("No sales data to process for stores.")
        return pd.DataFrame(columns=['Magazine', 'Vanzari', 'Target', 'Procent din target'])

    # Agregeaza datele de vanzari pe magazin
    df_magazine = df_sales.groupby('store', as_index=False)['total_sales'].sum()

    # Incarca datele target pentru magazine
    df_target_magazine = pd.read_excel(TARGET_MAGAZINE_PATH)

    # combinam datele de vanzari cu datele target
    df_magazine = pd.merge(df_magazine, df_target_magazine, left_on='store', right_on='magazin', how='left')

    # Daca nu exista coloana 'target', punem 0
    if 'target' not in df_magazine.columns:
        df_magazine['target'] = 0

    # Calculeaza procentul din target realizat pentru fiecare magazin
    df_magazine['Procent din target'] = df_magazine.apply(
        lambda row: (row['total_sales'] / row['target'] * 100) if row['target'] != 0 else 0,
        axis=1
    )

    # Redenumeste coloanele pentru a se potrivi cu ieșirea așteptată
    df_magazine = df_magazine.rename(columns={'total_sales': 'Vanzari', 'target': 'Target', 'store': 'Magazin'})
    logging.debug(f"Processed store data: {df_magazine.head()}")
    return df_magazine

