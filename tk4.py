"""Написать приложение, которое загружает веб-страницу, указанную в варианте, извлекает из ее HTML-кода некоторые данные и выводит их на экран. Ничего лишнего выводиться не должно.
Способ извлечения данных – любой. Хоть регулярные выражения, хоть библиотека какая угодно. Лишь бы работало.

Вариант9: https://price59.ru/ Название рубрики и список подрубрик (до слова «еще…»)
"""

import re
import requests

session = requests.session()
url = "https://price59.ru/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/87.0.4280.88 Safari/537.36"}

html = session.get(url, headers=headers).text

sections = re.findall('<div class="catalog_wrapper.+?">(.+?)</div>', html, flags=re.DOTALL)

for section in sections:
    titleMatch = re.search('<a href="/catalog/[\w-]+/">([А-Яа-я\-\s]+)</a>', section)
    if titleMatch:
        title = titleMatch.group(1)
        subcategories = re.findall('<a href="/catalog/[\w-]+/.+?/">([А-Яа-я\-\s]+)</a>,', section)
        print("Рубрика: " + title + " \nПодрубрики:")
        for subcategory in subcategories:
            print("\t- " + subcategory)
        print("=====================================================")

exit()
