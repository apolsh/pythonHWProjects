"""Вариант14, Задача1: Дана последовательность из 10 строк.
Определить сколько из них обладают длиной большей чем m"""
stringArray = []
m = 0
# get 10 input string
for i in range(1, 11):
    stringArray.append(input("Введите строку№{0}: ".format(i)))
# get m
while True:
    try:
        m = int(input("Введите целое число: "))
    except ValueError:
        print("Вы ввели значение на являющееся целым числом, попробуйте еще раз.")
        continue
    else:
        break
# count string length greater than m
count = 0
for string in stringArray:
    if len(string) > m:
        count += 1
# print result
print("{0} строк обладают длиной большей чем {1}".format(count, m))
