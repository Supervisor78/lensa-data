
# Lensa Data Dashboard

Lensa Data Dashboard este o aplicație web dezvoltată cu Streamlit, care oferă vizualizări interactive și analiză a datelor. Aplicația utilizează o bază de date mockup SQLite și fișiere Excel pentru procesarea datelor. Aplicația este deja disponibilă pe Streamlit Cloud.

---

## Funcționalități

- **Vizualizări interactive**:
- Grafice de tip bară și plăcintă utilizând Matplotlib.
- Hărți dinamice realizate cu Folium și Streamlit Folium.
- **Manipularea datelor**:
- Citește date din baza de date `mockup_database.db` (SQLite).
- Procesează fișiere Excel precum `Target categorii.xlsx` și `Target magazine.xlsx`.
- **Opțiuni configurabile**:
- Posibilitatea de a activa/dezactiva bonusurile prin setările din fișierul `config.py`.

---

## Link-ul Aplicației

Aplicația este disponibilă online și poate fi accesată aici:

**[Accesează Lensa Data Dashboard](https://lensa-board.streamlit.app/)**

---

## Structura Proiectului

```
src/
├── LICENSE
├── requirements.txt
├── Target categorii.xlsx
├── Target magazine.xlsx
├── database.py
├── __init__.py
├── README.md
├── main.py
├── mockup_database.db
├── ui/
│   ├── __init__.py
│   ├── style.css
│   ├── components/
│   │   ├── charts.py
│   │   ├── filters.py
│   ├── pages/
│   │   ├── categorii.py
│   │   ├── magazine.py
│   ├── translations/
│       ├── __init__.py
│       ├── ro.json
├── logic/
│   ├── config.py
│   ├── __init__.py
│   ├── data_processing.py
│   ├── queries.py
├── utils/
│   ├── helpers.py
```

---

## Instalare (Rulare Locală)

Pentru a rula aplicația pe calculatorul local:

1. **Clonează Repozitoriul**:
```bash
git clone https://github.com/Supervisor78/lensa-data.git
cd lensa-data
```

2. **Creează un Mediu Virtual**:
```bash
python -m venv venv
source venv/bin/activate    # Pentru Windows: venv\Scripts\activate
```

3. **Instalează Dependențele**:
```bash
pip install -r requirements.txt
```

4. **Rulează Aplicația**:
```bash
streamlit run main.py
```

5. **Accesează Aplicația**:
- Deschide browser-ul și navighează la `http://localhost:8501`.

---

## Configurație

Aplicația utilizează un fișier de configurare (`config.py`) pentru a gestiona căile fișierelor și setările. Asigură-te că următoarele fișiere sunt în directorul principal al proiectului:
- `mockup_database.db`
- `Target categorii.xlsx`
- `Target magazine.xlsx`

---

## Baza de Date SQLite

Fișierul `mockup_database.db` este inclus în repository-ul GitHub și este accesat direct din mediul Streamlit Cloud, fără a fi necesară copierea în alte locații.



---

## Deploy pe Streamlit Cloud

Aplicația este implementată folosind pașii următori:

1. Adaugă un fișier `requirements.txt` care să conțină toate dependențele necesare:
```text
streamlit==1.40.2
matplotlib==3.9.3
pandas==2.2.3
numpy==2.0.2
openpyxl==3.1.5
folium==0.19.0
streamlit_folium==0.23.2
requests==2.32.3
```

2. Urcă codul și fișierele pe GitHub.

3. Conectează repo-ul la Streamlit Cloud și setează `main.py` ca punct de start.

---

## Probleme Cunoscute

- **Sistem de Fișiere Read-Only**: Modificările în baza de date `mockup_database.db` în timpul utilizării aplicației pe Streamlit Cloud nu vor persista între sesiuni.
- **Fișiere Mari**: Asigură-te că fișierele urcate respectă limitele de dimensiune impuse de Streamlit Cloud.

---

## Îmbunătățiri Viitoare

- **Migrarea Bazei de Date**: Mutarea bazei de date `mockup_database.db` într-un serviciu de baze de date găzduit în cloud pentru stocare persistentă.
- **Vizualizări Avansate**: Adăugarea de grafice mai interactive folosind librării precum Plotly.

---

## Contact

Pentru întrebări sau feedback, mă poți contacta:

- **Nume**: Damian Șerban
- **Email**: serban.damian94@gmail.com
- **GitHub**: [Supervisor78](https://github.com/Supervisor78)
