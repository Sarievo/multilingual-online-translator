import sys
import requests
from bs4 import BeautifulSoup

saved_results = []


def log_print(s=''):
    saved_results.append(s)
    print(s)


def get_page(lang_choice, word_choice):
    url = f"https://context.reverso.net/translation/{lang_choice}/{word_choice}"
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    if page.status_code != 200:
        page = requests.get(url, headers=headers)
    return page


def filter_page(page_data) -> (list, list, list):
    global word
    soup = BeautifulSoup(page_data.content, 'html.parser')
    terms = [t.text for t in soup.find_all('span', 'display-term')]
    if len(terms) == 0:
        print(f"Sorry, unable to find {word}")
        exit()
    examples_src = [t.text.strip() for t in soup.find_all('div', 'src')]
    examples_trg = [t.text.strip() for t in soup.find_all('div', 'trg')]
    return terms, examples_src, examples_trg


def format_print(limit: int, terms: list, examples_src: list, examples_trg: list):
    global trg_lang
    log_print(f"{trg_lang} Translations:")
    for i in range(min(limit, len(terms))):
        log_print(terms[i])

    log_print(f"\n{trg_lang} Examples:")
    for i in range(min(limit, len(examples_src), len(examples_trg))):
        log_print(examples_src[i])
        log_print(examples_trg[i])
        log_print()
    log_print()


def print_translations(limit=5):
    data = get_page(f"{src_lang.lower()}-{trg_lang.lower()}", word)
    format_print(limit, *filter_page(data))


args = sys.argv
if len(args) != 4:
    print("Usage: <src_lang> <trg_lang> <word>")
    exit()
lang_list = ["Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese",
             "Dutch", "Polish", "Portuguese", "Romanian", "Russian", "Turkish"]
src_lang, trg_lang, word = args[1].capitalize(), args[2].capitalize(), args[3]
if src_lang not in lang_list:
    print(f"Sorry, the program doesn't support {src_lang}")
    exit()
if trg_lang not in lang_list and trg_lang != "All":
    print(f"Sorry, the program doesn't support {trg_lang}")
    exit()
try:
    if trg_lang == 'All':
        for lang in lang_list:
            if lang != src_lang:
                trg_lang = lang
                print_translations(limit=1)
    else:
        print(f"You choose \"{trg_lang}\" as a language to translate \"{word}\".")
        print_translations()
    with open(f"{word}.txt", 'w', encoding='utf-8') as file:
        for line in saved_results:
            file.write(f"{line}\n")
except ConnectionError:
    print("Something wrong with your internet connection")
