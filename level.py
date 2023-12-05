import streamlit as st

def get_level(selected_language, languages, selected_form, forms, levels):
    selected_level = st.selectbox("Wybierz stopień studiów: ", levels)

    if selected_language == languages[0]:
        if selected_form == forms[0]:
            if selected_level == "studia pierwszego stopnia (inżynier)":
                url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/40"
            elif selected_level == "studia pierwszego stopnia (licencjat)":
                url = "https://sylabus.sggw.edu.pl/pl/1/19/3/2/40"
            elif selected_level == "studia drugiego stopnia (magister inżynier)":
                url = "https://sylabus.sggw.edu.pl/pl/1/19/3/6/40"
            elif selected_level == "studia drugiego stopnia (magister)":
                url = "https://sylabus.sggw.edu.pl/pl/1/19/3/3/40"
            elif selected_level == "jednolite studia magisterskie":
                url = "https://sylabus.sggw.edu.pl/pl/1/19/3/7/40"
            else: KeyError("brak linku do strony")
        else:
            if selected_level == "studia pierwszego stopnia (inżynier)":
                url = "https://sylabus.sggw.edu.pl/pl/1/19/4/4/40"
            elif selected_level == "studia pierwszego stopnia (licencjat)":
                url = "https://sylabus.sggw.edu.pl/pl/1/19/4/2/40"
            elif selected_level == "studia drugiego stopnia (magister inżynier)":
                url = "https://sylabus.sggw.edu.pl/pl/1/19/4/6/40"
            elif selected_level == "studia drugiego stopnia (magister)":
                url = "https://sylabus.sggw.edu.pl/pl/1/19/4/3/40"
            else: KeyError("brak linku do strony")
    else:
        if selected_level == "studia pierwszego stopnia (inżynier)": 
            url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/46"
        elif selected_level == "studia pierwszego stopnia (licencjat)":
            url = "https://sylabus.sggw.edu.pl/pl/1/19/3/2/46"
        elif selected_level == "studia drugiego stopnia (magister inżynier)":
            url = "https://sylabus.sggw.edu.pl/pl/1/19/3/6/46"
        elif selected_level == "studia drugiego stopnia (magister)":
            url = "https://sylabus.sggw.edu.pl/pl/1/19/3/3/46"
        elif selected_level == "jednolite studia magisterskie":
            url = "https://sylabus.sggw.edu.pl/pl/1/19/3/7/46"
        else: KeyError("brak linku do strony")
    
    return selected_level, url