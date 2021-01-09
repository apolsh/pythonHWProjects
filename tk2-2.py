"""Инвестиционный проект открытие кофейни:
Первоначальные вложения:
    Кофемашина: 200 000 рублей
    Оборудование витрины: 50 000 рублей

Доход:
    Кофе - 50 рублей за кружку
Расходы:
    Постоянные расходы:
        Аренда помещения: 10 000 рублей * 12 = 120 000 рублей в год
        Оплата сотруднику: 25 000 рублей * 12 = 300 000 рублей в год
        Обслуживание кофемашины: 20 000 рублей в год
    Переменные расходы:
        Стаканчик - 5 рублей
        Вода - 10 рублей * 0.5л = 2 рубля
        Кофе - 0.5 рублей * 7грамм = 3.5 рублей
        Сахар - 0.15 рублей * 14 грамм (2 ложки) = 2.1 рублей
        Молоко - 200 * 0.05 = 10 рублей

Ожидаемый клиентопоток в день 50 человек (кружек кофе) в день
выгода с каждой кружки кофе: 50 - (5 + 3.5 + 2.1 + 2 + 10) = 27.4

В соответствии с информацией с сайта https://www.sravni.ru/, средняя ставка по вкладу сроком на год находится
на уровне 6% - эту ставку, примем это значение за ставку дисконтирования
"""
import warnings
from functools import reduce
from itertools import accumulate
import numpy as np
warnings.filterwarnings("ignore", category=DeprecationWarning)

initialCosts = 250000.0
projectDuration = 5
cupsToSell = 50
costOfCoffee = 50
yearIncome = cupsToSell * costOfCoffee * 365
yearConsumption = cupsToSell * 22.6 * 365 + 20000 + 420000
discountRate = 0.06

# NPV
incomeByPeriods = [yearIncome] * projectDuration
outcomeByPeriods = ([yearConsumption] * projectDuration)
netValueByPeriods = list(map(lambda i, o: i - o, incomeByPeriods, outcomeByPeriods))
NPVByPeriods = list(map(lambda i: netValueByPeriods[i] / ((1 + discountRate) ** (i + 1)), range(0, projectDuration)))
NPVAccumulated = list(accumulate(NPVByPeriods))
NPV = NPVAccumulated[len(NPVAccumulated) - 1] - initialCosts
paybackPeriod = next(x for x, val in enumerate(NPVAccumulated) if val > initialCosts)
# дисконтированный срок окупаемости
DPP = paybackPeriod + (1 - ((NPVAccumulated[paybackPeriod] - initialCosts) / NPVByPeriods[paybackPeriod]))
# IRR
IRR = np.irr([initialCosts * -1] + netValueByPeriods)

print("NPV = {0} - сумма потока платежей, приведённых к сегодняшнему дню. В нашем случае NPV положительный, "
      "значит при заданных параметрах (срок 5 лет, ставка дисконтирования = 6%) по итогу принесет хоть и небольшую, "
      "но прибыль.".format(round(NPV, 2)))
print("DPP = {0} - дисконтированный срок окупаемости проекта. В нашем случае проект окупается через {0} "
      "года, с учетом приведения потоков платежей, приведенных к сегодняшнему дню.".format(round(DPP, 2)))
print("IRR = {0} - внутренняя норма доходности, т.е. только при ставке дисконтирования = {0}% и выше наш проект "
      "сможет окупиться".format(round(IRR, 4)))
print("Таким образом, наш проект окупается, но находится на грани, а с учётом снижения спроса на общепит в "
      "условиях пандемии, я бы не решился вкладывать свои финансы в подобный проект :).")
