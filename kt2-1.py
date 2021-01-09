import pickle
import re

linesRead = ""

while True:
    filepath = input("Введите путь до текстового файла для анализа: ")
    try:
        with open(filepath, "r", encoding='utf-8') as textFile:
            linesRead = textFile.readlines()
    except FileNotFoundError:
        print("По указанному пути не существует файла. Попробуйте еще раз.")
    else:
        break

# 1. Выполнить количественный анализ текста
if len(linesRead) == 0:
    print("Указанный файл пустой.")
    exit()
preparedText = ''.join(linesRead).strip()

analysisResult = {}
punctuationMarks = ['.', ',', '!', '?', '-']

sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", preparedText)
words = re.sub(r"\.|\?|\!|,|\(|\)", "", preparedText).split()
analysisResult["Всего слов"] = len(words)
analysisResult["Всего предложений"] = len(sentences)

# sentence counting
sentencesWithLength = map(lambda s: (s, len(s.split())), sentences)
analysisResult["Предложения"] = list(sentencesWithLength)

# word counting
wordSizes = {}
for word in words:
    wordSizes[word] = wordSizes.get(word, len(list(word)))
analysisResult["Слова"] = wordSizes

# punctuation mark counting
marks = {}
for mark in punctuationMarks:
    count = preparedText.count(mark)
    if count > 0:
        marks[mark] = count
analysisResult["Знаки препинания"] = marks

# 2. Сохранить полученный объект в двоичный файл с помощью модуля pickle, затем загрузить из файла
with open("temp.bin", "wb") as tempFile:
    pickle.dump(analysisResult, tempFile)

with open("temp.bin", "rb") as tempFile:
    someInfo = pickle.load(tempFile)

# 3. Вывести рассчитанную статистику на экран в удобоваримом виде.
print(analysisResult)

# 4. Разбить текст на абзацы по n предложений (n вводится с клавиатуры).
paragraphs = []
n = 0
while True:
    try:
        n = int(input("Введите целое число: "))
    except ValueError:
        print("Вы ввели значение на являющееся целым числом, попробуйте еще раз.")
        continue
    else:
        break
paragraphs = [sentences[x:x + n] for x in range(0, len(sentences), n)]
paragraphs = list(map(lambda p: "".join(p), paragraphs))

# 5. Абзацы отсортировать по количеству слов в них.
paragraphs.sort(key=lambda p: len(p.split()))
print(paragraphs)

# 6. Сохранить полученный текст в текстовый файл.
with open("output.txt", "w", encoding='utf-8') as saveFile:
    for paragraph in paragraphs:
        print(paragraph, file=saveFile, end="\n")
