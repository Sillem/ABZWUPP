import streamlit as st

def get_form(bs, selected_language, languages, forms):
    selected_form = st.selectbox("Wybierz formę studiów: ", forms)

    if selected_language == languages[0]:
        if selected_form == forms[0]:
            url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/40"
            links_level = bs.find_all('li', text=lambda text: text and ('stopnia' in text or 'magister' in text))
            levels = [level.get_text(strip = True) for level in links_level]
        else:
            url = "https://sylabus.sggw.edu.pl/pl/1/19/4/4/40"
            links_level = bs.find_all('li', text=lambda text: text and ('stopnia' in text or 'magister' in text))
            levels = [level.get_text(strip = True) for level in links_level]
            levels.remove("jednolite studia magisterskie")
    else:
        url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/46"
        links_level = bs.find_all('li', text=lambda text: text and ('stopnia' in text or 'magister' in text))
        levels = [level.get_text(strip = True) for level in links_level]

    return selected_form, url, levels