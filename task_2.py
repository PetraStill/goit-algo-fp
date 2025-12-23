"""
Програма для візуалізації фрактала «дерево Піфагора» за допомогою рекурсії та модуля turtle.

Користувач задає рівень рекурсії, після чого на екрані малюється стилізоване дерево Піфагора:
- функція draw_tree рекурсивно малює стовбур і дві гілки під кутом 45°;
- функція main налаштовує вікно, черепашку та запускає малювання.
"""

import turtle
import math


def draw_tree(t: turtle.Turtle, length: float, level: int) -> None:
    """Рекурсивно малює гілки дерева Піфагора."""
    if level == 0:
        return

    # Малюємо стовбур поточної гілки
    t.forward(length)

    # Малюємо ліву гілку
    t.left(45)
    draw_tree(t, length * math.sqrt(2) / 2, level - 1)

    # Малюємо праву гілку
    t.right(90)
    draw_tree(t, length * math.sqrt(2) / 2, level - 1)

    # Повертаємося в початкову позицію й орієнтацію
    t.left(45)
    t.backward(length)


def main() -> None:
    """Запитує рівень рекурсії та малює дерево Піфагора за допомогою turtle."""
    level = int(input("Введіть рівень рекурсії (наприклад, 8–12): "))

    screen = turtle.Screen()
    screen.title("Дерево Піфагора")

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.color("#8B0000")  # темно-червоний колір ліній

    # Стартуємо знизу екрана, напрямок — вгору
    t.penup()
    t.goto(0, -250)
    t.setheading(90)
    t.pendown()

    draw_tree(t, 120, level)

    screen.mainloop()


if __name__ == "__main__":
    main()
