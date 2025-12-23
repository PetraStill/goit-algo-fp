"""
Модуль будує бінарне дерево з вузлів Node та візуалізує два типи обходів:
обхід у глибину (DFS) і обхід у ширину (BFS).

Для обходів використовуються стек і черга (без рекурсії).
Порядок відвідування вузлів відображається за допомогою градієнта кольорів
від темних до світлих у форматі HEX (RGB), що дає змогу візуально бачити
послідовність обходу.
"""

import uuid
from collections import deque
from typing import List, Optional, Dict, Tuple

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    """
    Представляє вузол бінарного дерева.

    Зберігає значення, колір для візуалізації та унікальний ідентифікатор,
    який використовується як id вузла в графі NetworkX.
    """

    def __init__(self, key: int, color: str = "#9E9E9E") -> None:
        # Сірий колір позначає стан "ще не відвідано"
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.val: int = key
        self.color: str = color
        self.id: str = str(uuid.uuid4())


def add_edges(
    graph: nx.DiGraph,
    node: Optional[Node],
    pos: Dict[str, Tuple[float, float]],
    x: float = 0.0,
    y: float = 0.0,
    layer: int = 1,
) -> nx.DiGraph:
    """
    Додає вузли й ребра дерева до графа NetworkX і задає їхні координати.

    :param graph: Орієнтований граф NetworkX, що будується.
    :param node: Поточний вузол дерева, з якого продовжується побудова.
    :param pos: Словник позицій вузлів у форматі {id: (x, y)}.
    :param x: Поточна координата x для вузла.
    :param y: Поточна координата y для вузла.
    :param layer: Поточний рівень глибини в дереві (корінь = 1).
    :return: Оновлений граф NetworkX.
    """
    if node is not None:
        # Додаємо поточний вузол до графа з кольором і міткою
        graph.add_node(node.id, color=node.color, label=node.val)

        # Додаємо лівого нащадка
        if node.left:
            graph.add_edge(node.id, node.left.id)
            left_x = x - 1 / 2 ** layer
            pos[node.left.id] = (left_x, y - 1)
            add_edges(graph, node.left, pos, x=left_x,
                      y=y - 1, layer=layer + 1)

        # Додаємо правого нащадка
        if node.right:
            graph.add_edge(node.id, node.right.id)
            right_x = x + 1 / 2 ** layer
            pos[node.right.id] = (right_x, y - 1)
            add_edges(graph, node.right, pos, x=right_x,
                      y=y - 1, layer=layer + 1)

    return graph


def draw_tree(tree_root: Node, title: str = "") -> None:
    """
    Візуалізує бінарне дерево, починаючи з кореневого вузла.

    Створює граф NetworkX, обчислює позиції вузлів та малює дерево
    за поточними кольорами вузлів.
    """
    tree = nx.DiGraph()
    pos: Dict[str, Tuple[float, float]] = {tree_root.id: (0.0, 0.0)}

    # Перетворюємо дерево вузлів Node у граф NetworkX для подальшої візуалізації
    add_edges(tree, tree_root, pos)

    colors = [node_data["color"] for _, node_data in tree.nodes(data=True)]
    labels = {node_id: node_data["label"]
              for node_id, node_data in tree.nodes(data=True)}

    plt.clf()
    if title:
        plt.title(title)
    nx.draw(
        tree,
        pos=pos,
        labels=labels,
        arrows=False,
        node_size=2500,
        node_color=colors,
    )
    plt.axis("off")


def rgb_hex(r: int, g: int, b: int) -> str:
    """
    Повертає колір у форматі HEX (#RRGGBB) за значеннями R, G, B (0–255).
    """
    return f"#{r:02X}{g:02X}{b:02X}"


def gradient_colors(n: int, start_hex: str = "#0B1F3A", end_hex: str = "#CFE8FF") -> List[str]:
    """
    Генерує n кольорів у форматі HEX, утворюючи градієнт від темного до світлого.

    :param n: Кількість кольорів у градієнті.
    :param start_hex: Початковий (темніший) колір у форматі HEX.
    :param end_hex: Кінцевий (світліший) колір у форматі HEX.
    :return: Список з n рядків-колірних значень HEX.
    """
    if n <= 0:
        return []

    def parse(h: str) -> Tuple[int, int, int]:
        h = h.lstrip("#")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    sr, sg, sb = parse(start_hex)
    er, eg, eb = parse(end_hex)

    if n == 1:
        return [rgb_hex(sr, sg, sb)]

    colors: List[str] = []
    for i in range(n):
        t = i / (n - 1)
        r = round(sr + (er - sr) * t)
        g = round(sg + (eg - sg) * t)
        b = round(sb + (eb - sb) * t)
        colors.append(rgb_hex(r, g, b))
    return colors


def dfs_order_stack(root: Optional[Node]) -> List[Node]:
    """
    Обчислює порядок обходу дерева в глибину (DFS) без рекурсії, використовуючи стек.

    Порядок: Root → Left → Right (правий нащадок додається до стека першим).
    """
    if root is None:
        return []

    order: List[Node] = []
    stack: List[Node] = [root]

    while stack:
        node = stack.pop()
        order.append(node)

        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return order


def bfs_order_queue(root: Optional[Node]) -> List[Node]:
    """
    Обчислює порядок обходу дерева в ширину (BFS) без рекурсії, використовуючи чергу.
    """
    if root is None:
        return []

    order: List[Node] = []
    q: deque[Node] = deque([root])

    while q:
        node = q.popleft()
        order.append(node)

        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)

    return order


def reset_colors(root: Optional[Node], default: str = "#9E9E9E") -> None:
    """
    Скидає кольори всіх вузлів дерева до значення за замовчуванням.

    Обхід виконується в ширину (черга), без рекурсії.
    """
    if root is None:
        return

    q: deque[Node] = deque([root])
    seen: set[str] = set()

    while q:
        node = q.popleft()
        if node.id in seen:
            continue
        seen.add(node.id)

        node.color = default

        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)


def visualize_traversal(
    root: Optional[Node],
    order: List[Node],
    caption: str,
    pause_sec: float = 0.8,
) -> None:
    """
    Візуалізує покроковий обхід дерева відповідно до заданого порядку вузлів.

    Для кожного кроку вузол підсвічується унікальним кольором з градієнта,
    після чого дерево перемальовується.
    """
    if root is None or not order:
        print("Немає даних для візуалізації обходу.")
        return

    colors = gradient_colors(
        len(order), start_hex="#0B1F3A", end_hex="#CFE8FF")

    plt.ion()
    plt.figure(figsize=(10, 6))

    for step, (node, col) in enumerate(zip(order, colors), start=1):
        node.color = col
        draw_tree(
            root,
            title=f"{caption} — крок {step}/{len(order)} (відвідано: {node.val})",
        )
        plt.pause(pause_sec)

    plt.ioff()
    plt.show()


# ====== Приклад дерева ======
if __name__ == "__main__":
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)

    # DFS
    reset_colors(root)
    dfs = dfs_order_stack(root)
    visualize_traversal(root, dfs, caption="DFS (стек)")

    # BFS
    reset_colors(root)
    bfs = bfs_order_queue(root)
    visualize_traversal(root, bfs, caption="BFS (черга)")
