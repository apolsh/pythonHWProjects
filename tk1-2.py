"""Вариант14, Задача2: С клавиатуры вводится текст, содержащий слова с повторяющимися буквами.
Изменить регистр повторяющихся символов.
Результат оформить в виде функции: на входе исходный текст, на выходе обработанный"""
import re


def repeatedToUppercase(inputText):
    """
    Функция для применяющая верхний регистр для повторяющихся символов в тексте
    :rtype: String
    :type inputText: String
    """
    pattern = r"(?:(\w))\1{1,}"

    def toUpperCase(matchObj):
        upper_cased = ''
        for char in matchObj.group(0):
            upper_cased += char.capitalize()
        return upper_cased

    regexp = re.compile(pattern)
    return regexp.sub(toUpperCase, inputText)


def main():
    some_string = input("Введите строку для фоматирования: ")
    #some_string = "The mission of tttthe Pythoooon Softwaree Foundatiiiiion is to promoote"
    print(repeatedToUppercase(some_string))


main()
