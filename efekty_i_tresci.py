from bs4 import BeautifulSoup
import requests
from utils import remove_char


payload = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


def get_effects_and_content(chosen_id):

    doc_url = "https://sylabus.sggw.edu.pl/pl/document/" + chosen_id + ".jsonHtml"
    response = requests.request("GET", doc_url, headers=headers, data=payload)
    html = response.json()["html"]

    bs4 = BeautifulSoup(html, "html.parser")
    # print(bs4.prettify())
    course_content = ""
    learning_effects = ""

    h1s = bs4.find_all("h1")
    for h1 in h1s:
        if h1.get_text().strip() == "Efekty uczenia się dla przedmiotu":
            print("-----EFEKTY UCZENIA SIE-----")
            print(h1)
            efekty_tag = h1.find_next()

            for i, item in enumerate(efekty_tag.find_all("td", class_="code")):
                if "row_code" not in item["class"] and "row_header" not in item["class"]:
                    if item.find("span") is None:
                        print(i, item.find_next().get_text().strip())
                        learning_effects += item.find_next().get_text().strip() + " "

        if h1.get_text().strip() == "Treści programowe":
            print("-----TREŚCI PROGRAMOWE-----")
            # print(h1)
            tresc_tag = h1.find_next()
            # print(tresc_tag)

            for i, item in enumerate(tresc_tag.find_all("td", class_="code")):
                if "row_code" not in item["class"] and "row_header" not in item["class"]:
                    # print(i, item)
                    the_text = item.find_next().get_text().strip()
                    print(the_text)
                    course_content += the_text + " "
    
    return learning_effects, course_content

def get_codes(chosen_id):
    
    doc_url = "https://sylabus.sggw.edu.pl/pl/document/" + chosen_id + ".jsonHtml"
    response = requests.request("GET", doc_url, headers=headers, data=payload)
    html = response.json()["html"]

    bs4 = BeautifulSoup(html, "html.parser")
    codes_and_descriptions1 = []
    codes_and_descriptions2 = []

    print("-----KODY-----")
    for item2 in bs4.find_all("span", class_="popup"):
        if item2.get("data-bs-original-title") is not None:
            code = remove_char(item2.get_text().strip(), ",")
            code_description = item2.get("data-bs-original-title")
            codes_and_descriptions1.append((code, code_description))
            print(code)
            print(code_description)
        if item2.get("title") is not None:
            code = remove_char(item2.get_text().strip(), ",")
            code_description = item2.get("title")
            codes_and_descriptions2.append((code, code_description))
            print(code)
            print(code_description)
        else:
            print("No popup title found")

    return codes_and_descriptions2