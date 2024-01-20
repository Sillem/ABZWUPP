@echo off
py -m pip install pandas matplotlib streamlit numpy scikit-learn mplcursors plotly openpyxl bs4 kaleido
python -m pip install pandas matplotlib streamlit numpy scikit-learn mplcursors plotly openpyxl bs4 kaleido
streamlit run GUI_class.py
pause