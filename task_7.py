"""
Модуль моделює кидання двох гральних кубиків методом Монте-Карло.

Мета:
- Рахуємо частоти сум (2..12) за великої кількості симуляцій.
- Обчислюємо ймовірності сум за методом Монте-Карло.
- Порівнюємо отримані ймовірності з аналітичними значеннями (табличними для 2 кубиків).
- Створюємо підсумкову таблицю та будуємо графік для візуалізації.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt


@dataclass(frozen=True)
class DiceSimulationConfig:
    """Описує параметри симуляції кидків кубиків."""
    rolls_count: int = 200_000
    random_seed: int = 42


def get_analytical_probabilities() -> Dict[int, float]:
    """
    Створює аналітичний розподіл ймовірностей сум для двох чесних кубиків.

    Повертає:
        Словник {сума: ймовірність}.
    """
    # Створюємо кількість способів отримання кожної суми (всього 36 рівноймовірних пар).
    ways_by_sum = {
        2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6,
        8: 5, 9: 4, 10: 3, 11: 2, 12: 1,
    }
    total_outcomes = 36

    # Рахуємо ймовірності як ways/36.
    return {sum_value: ways / total_outcomes for sum_value, ways in ways_by_sum.items()}


def roll_two_dice_sum() -> int:
    """
    Обчислює суму значень двох незалежних кидків кубика (1..6).

    Повертає:
        Суму від 2 до 12.
    """
    first_die = random.randint(1, 6)
    second_die = random.randint(1, 6)
    return first_die + second_die


def run_monte_carlo_simulation(config: DiceSimulationConfig) -> Dict[int, float]:
    """
    Обчислює ймовірності сум 2..12 за методом Монте-Карло.

    Параметри:
        config: конфігурація симуляції (кількість кидків, seed)

    Повертає:
        Словник {сума: ймовірність_Монте_Карло}.
    """
    if config.rolls_count <= 0:
        raise ValueError("rolls_count має бути додатним цілим числом.")

    # Створюємо відтворюваність результатів.
    random.seed(config.random_seed)

    # Створюємо лічильник частот для сум 2..12.
    occurrences_by_sum: Dict[int, int] = {sum_value: 0 for sum_value in range(2, 13)}

    # Рахуємо симуляцію великої кількості кидків.
    for _ in range(config.rolls_count):
        sum_value = roll_two_dice_sum()
        occurrences_by_sum[sum_value] += 1

    # Рахуємо ймовірності як частоту / кількість кидків.
    return {sum_value: count / config.rolls_count for sum_value, count in occurrences_by_sum.items()}


def build_comparison_rows(
    monte_carlo_probabilities: Dict[int, float],
    analytical_probabilities: Dict[int, float],
) -> List[Tuple[int, float, float, float]]:
    """
    Створює рядки порівняльної таблиці для сум 2..12.

    Повертає список кортежів:
        (сума, імовірність_MC, імовірність_аналітична, абсолютна_різниця)
    """
    # Створюємо впорядковані рядки для виводу/таблиці.
    rows: List[Tuple[int, float, float, float]] = []
    for sum_value in range(2, 13):
        mc_probability = monte_carlo_probabilities[sum_value]
        analytical_probability = analytical_probabilities[sum_value]
        absolute_difference = abs(mc_probability - analytical_probability)
        rows.append((sum_value, mc_probability, analytical_probability, absolute_difference))

    return rows


def print_comparison_table(rows: List[Tuple[int, float, float, float]]) -> None:
    """
    Друкує порівняльну таблицю у консоль.
    """
    # Створюємо заголовок.
    header = f"{'Сума':>4} | {'MC ймовірність':>14} | {'Аналітична':>11} | {'|Різниця|':>10}"
    print(header)
    print("-" * len(header))

    # Рахуємо та виводимо рядки.
    for sum_value, mc_probability, analytical_probability, absolute_difference in rows:
        print(
            f"{sum_value:>4} | "
            f"{mc_probability:>14.6f} | "
            f"{analytical_probability:>11.6f} | "
            f"{absolute_difference:>10.6f}"
        )


def plot_probabilities(rows: List[Tuple[int, float, float, float]], save_path: str = "") -> None:
    """
    Будує графік ймовірностей сум (Монте-Карло та аналітичних) для порівняння.
    
    Параметри:
        rows: рядки порівняльної таблиці
        save_path: шлях для збереження графіка (якщо вказано)
    """
    # Створюємо дані для осей.
    sums = [row[0] for row in rows]
    mc_values = [row[1] for row in rows]
    analytical_values = [row[2] for row in rows]

    # Створюємо графік.
    plt.figure(figsize=(10, 6))
    plt.plot(sums, mc_values, marker="o", linestyle="-", linewidth=2, markersize=8, label="Монте-Карло")
    plt.plot(sums, analytical_values, marker="x", linestyle="--", linewidth=2, markersize=8, label="Аналітичні")
    plt.title("Ймовірності сум при киданні двох кубиків", fontsize=14)
    plt.xlabel("Сума", fontsize=12)
    plt.ylabel("Ймовірність", fontsize=12)
    plt.xticks(sums)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()
    
    # Зберігаємо графік, якщо вказано шлях.
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"\nГрафік збережено: {save_path}")
    
    plt.show()


def main() -> None:
    """Запускає симуляцію, порівняння та візуалізацію результатів."""
    # Створюємо конфігурацію симуляції.
    simulation_config = DiceSimulationConfig(rolls_count=200_000, random_seed=42)

    # Рахуємо ймовірності методом Монте-Карло.
    monte_carlo_probabilities = run_monte_carlo_simulation(simulation_config)

    # Створюємо аналітичні ймовірності для порівняння.
    analytical_probabilities = get_analytical_probabilities()

    # Створюємо порівняльні рядки таблиці.
    comparison_rows = build_comparison_rows(monte_carlo_probabilities, analytical_probabilities)

    # Виводимо порівняльну таблицю.
    print(f"Симуляція: {simulation_config.rolls_count} кидків, seed={simulation_config.random_seed}")
    print_comparison_table(comparison_rows)

    # Будуємо графік для візуалізації та зберігаємо його.
    plot_probabilities(comparison_rows, save_path="task_7_chart.png")


if __name__ == "__main__":
    main()
