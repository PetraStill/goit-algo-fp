"""
Модуль реалізує вибір набору страв з максимальною сумарною калорійністю
в межах заданого бюджету двома підходами.
Перевіряє коректність бюджету та вхідних даних про страви.
Обчислює вибір страв жадібним алгоритмом за спаданням calories/cost.
Обчислює оптимальний вибір страв алгоритмом динамічного програмування (0/1 knapsack).
Обчислює сумарну вартість та сумарну калорійність для обраного набору страв.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(items: Dict[str, Dict[str, int]], budget: int) -> List[str]:
    """
    Перевіряє коректність бюджету та вхідних даних про страви.
    Створює ранжований список страв за спаданням співвідношення calories/cost.
    Обирає страви жадібним способом, не перевищуючи заданий бюджет.
    Формує та повертає список назв обраних страв.
    """
    # Перевіряємо коректність бюджету.
    if budget < 0:
        raise ValueError("Бюджет має бути невід’ємним.")

    # Створюємо список для ранжування страв.
    ranked: List[Tuple[str, float, int, int]] = []

    # Перевіряємо вхідні дані та додаємо страви до ранжування.
    for name, data in items.items():
        cost = int(data["cost"])
        calories = int(data["calories"])

        # Перевіряємо коректність вартості та калорійності.
        if cost <= 0:
            raise ValueError("Вартість має бути додатною.")
        if calories < 0:
            raise ValueError("Калорійність має бути невід’ємною.")

        # Додаємо кортеж (назва, ratio, вартість, калорійність).
        ranked.append((name, calories / cost, cost, calories))

    # Сортуємо страви за спаданням співвідношення calories/cost.
    ranked.sort(key=lambda x: x[1], reverse=True)

    # Створюємо список вибраних страв та задаємо залишок бюджету.
    chosen: List[str] = []
    remaining = budget

    # Обираємо страви, не перевищуючи залишок бюджету.
    for name, _ratio, cost, _calories in ranked:
        if cost <= remaining:
            chosen.append(name)
            remaining -= cost

    return chosen


def dynamic_programming(items: Dict[str, Dict[str, int]], budget: int) -> List[str]:
    """
    Перевіряє коректність бюджету та вхідних даних про страви.
    Створює та заповнює таблицю динамічного програмування для 0/1 knapsack.
    Відновлює оптимальний набір страв, що максимізує калорійність при заданому бюджеті.
    Формує та повертає список назв обраних страв.
    """
    # Перевіряємо коректність бюджету.
    if budget < 0:
        raise ValueError("Бюджет має бути невід’ємним.")

    # Створюємо списки назв, вартостей та калорійності.
    names = list(items.keys())
    costs = [int(items[n]["cost"]) for n in names]
    calories = [int(items[n]["calories"]) for n in names]

    # Перевіряємо коректність вартостей та калорійності.
    if any(c <= 0 for c in costs):
        raise ValueError("Вартість має бути додатною.")
    if any(cal < 0 for cal in calories):
        raise ValueError("Калорійність має бути невід’ємною.")

    # Створюємо таблицю dp для обчислення максимальної калорійності.
    n = len(names)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    # Обчислюємо dp: максимальну калорійність для кожного i та b.
    for i in range(1, n + 1):
        cost_i = costs[i - 1]
        cal_i = calories[i - 1]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]
            if cost_i <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost_i] + cal_i)

    # Відновлюємо оптимальний вибір страв.
    chosen: List[str] = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            chosen.append(names[i - 1])
            b -= costs[i - 1]

    chosen.reverse()
    return chosen


def total_cost_and_calories(items: Dict[str, Dict[str, int]], chosen: List[str]) -> Tuple[int, int]:
    """
    Перевіряє коректність назв обраних страв відносно вхідного словника items.
    Обчислює сумарну вартість та сумарну калорійність обраного набору страв.
    Повертає кортеж (сума вартості, сума калорій).
    """
    # Перевіряємо наявність кожної обраної страви у словнику items.
    if any(name not in items for name in chosen):
        raise KeyError("Список chosen містить назву, якої немає у items.")

    # Обчислюємо сумарну вартість та сумарну калорійність.
    cost_sum = sum(int(items[name]["cost"]) for name in chosen)
    cal_sum = sum(int(items[name]["calories"]) for name in chosen)

    return cost_sum, cal_sum


if __name__ == "__main__":
    # Задаємо бюджет та обчислюємо розв’язки двома підходами.
    budget = 100

    greedy_choice = greedy_algorithm(items, budget)
    dp_choice = dynamic_programming(items, budget)

    # Обчислюємо сумарні метрики для кожного підходу.
    g_cost, g_cal = total_cost_and_calories(items, greedy_choice)
    d_cost, d_cal = total_cost_and_calories(items, dp_choice)

    # Виводимо результати.
    print("Budget:", budget)
    print("Greedy:", greedy_choice, "| cost:", g_cost, "| calories:", g_cal)
    print("DP:    ", dp_choice, "| cost:", d_cost, "| calories:", d_cal)
