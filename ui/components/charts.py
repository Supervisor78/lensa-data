import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import pandas as pd
import folium
from streamlit_folium import st_folium


def show_bar_chart(df, x_col, y_col, title):
    if df.empty:
        st.warning("The dataset is empty.")
        return
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(x_col, sort=None),
        y=y_col,
        tooltip=[x_col, y_col]
    ).properties(title=title)
    st.altair_chart(chart, use_container_width=True)


def show_pie_chart(df, column, title="Pie Chart"):
    if df.empty:
        st.warning("The dataset is empty.")
        return

    # nu afiseaza NaN sau 0% in grafic
    df = df.dropna(subset=[column])  # Remove rows where `column` is NaN
    df = df[df[column] > 0]          # Remove rows where `column` is 0%

    # asigura ca datele filtrate sunt valide
    if df.empty:
        st.warning("No valid data to display in the pie chart.")
        return

    if 'Categorie' not in df.columns:
        st.error("Expected column 'Categorie' not found in the dataset.")
        return

    sizes = df[column]
    labels = df['Categorie']
    colors = plt.cm.Paired(range(len(sizes)))

    # asigura ca numarul de etichete corespunde numarului de felii de pie chart
    if len(sizes) != len(labels):
        raise ValueError("The number of labels does not match the number of pie chart slices.")

    # defineste culorile si explode pentru fiecare categorie
    explode = [0.1] * len(sizes)

    # creaza un grafic de tip pie chart
    fig, ax = plt.subplots(figsize=(10, 7))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=None, autopct='%1.1f%%', startangle=140,
        colors=colors, explode=explode, textprops={'fontsize': 8}
    )

    # adauga o legend pentru fiecare categorie
    ax.legend(
        wedges, labels, title="Legend", loc="center left",
        bbox_to_anchor=(1, 0.5), fontsize=8
    )

    # ajusteaza dimensiunea fontului pentru text si procente
    ax.set_title(title, pad=20, fontsize=14)

    # asigura ca aspectul este un cerc
    ax.axis('equal')

    # afiseaza graficul
    st.pyplot(fig)


def show_map(df, column, title="Romania Map"):
    if df.empty:
        st.warning("The dataset is empty.")
        return

    # Coordonatele orașelor din România menționate în setul de date
    city_coordinates ={
        "Bucharest": [44.4268, 26.1025],
        "Cluj-Napoca": [46.7712, 23.6236],
        "Timișoara": [45.7489, 21.2087],
        "Iași": [47.1585, 27.6014],
        "Constanța": [44.1598, 28.6348],
        "Brașov": [45.6579, 25.6012],
        "Oradea": [47.0722, 21.9213],
        "Sibiu": [45.7983, 24.1256],
        "Craiova": [44.3302, 23.7949],
        "Ploiești": [44.9365, 26.0136],
        "Arad": [46.1866, 21.3123],
        "Baia Mare": [47.6597, 23.5795],
        "Bacău": [46.5671, 26.9136],
        "Botoșani": [47.7459, 26.6695],
        "Galați": [45.4353, 28.0076],
        "Pitești": [44.8565, 24.8692],
        "Târgu Mureș": [46.5453, 24.5625],
        "Râmnicu Vâlcea": [45.1022, 24.3752],
        "Deva": [45.8777, 22.9168],
        "Suceava": [47.6435, 26.2526],
        "Zalău": [47.1855, 23.0587],
        "Alba Iulia": [46.0773, 23.5742],
        "Satu Mare": [47.7900, 22.8856],
        "Reșița": [45.3009, 21.8893],
        "Târgu Jiu": [45.0378, 23.2744],
        "Focșani": [45.6950, 27.1866],
        "Piatra Neamț": [46.9270, 26.3709],
        "Buzău": [45.1509, 26.8230],
        "Călărași": [44.2031, 27.3306],
        "Vaslui": [46.6383, 27.7297],
        "Slatina": [44.4304, 24.3718],
        "Giurgiu": [43.9037, 25.9699],
        "Drobeta-Turnu Severin": [44.6260, 22.6581]
    }


    # Creaza o harta a Romaniei
    romania_map = folium.Map(location=[45.9432, 24.9668], zoom_start=7)

    # Adauga markeri pentru fiecare oras cu procentul din target
    for index, row in df.iterrows():
        city = row['Magazin']  # Assuming 'Magazin' column contains city names
        percent = row[column]

        if city in city_coordinates:
            coords = city_coordinates[city]
            folium.CircleMarker(
                location=coords,
                radius=10,
                popup=f"{city}: {percent:.2f}%",
                color="blue",
                fill=True,
                fill_color="blue",
            ).add_to(romania_map)

    # afiseaza harta
    st_folium(romania_map, width=700, height=500)
