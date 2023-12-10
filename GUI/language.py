import streamlit as st

# Wybór języka studiów
def get_language(bs):
    links_languages = bs.find_all('li', text = lambda text: text and 'prowadzone' in text)
    languages = [link.get_text(strip = True) for link in links_languages]
    selected_language = st.selectbox("Wybierz język studiów: ", languages)

    if selected_language == languages[0]:
        url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/40"
        links_form = bs.find_all('li', text = lambda text: text and 'stacjonarne' in text)
        forms = [form.get_text(strip = True) for form in links_form]
    else:
        url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/46"
        links_form = bs.find_all('li', text = lambda text: text and 'stacjonarne' in text)
        forms = [form.get_text(strip = True) for form in links_form]
        forms.remove("studia niestacjonarne")

    return selected_language, languages, forms, url