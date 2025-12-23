"""
Модуль візуалізує бінарну купу, подану у вигляді масиву,
у формі бінарного дерева з використанням бібліотек networkx та matplotlib.

Купа інтерпретується як повне бінарне дерево:
для індексу i лівий нащадок має індекс 2*i + 1, правий — 2*i + 2.
"""

import uuid
from typing import Dict, Tuple, Optional, List

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    """
    Представляє вузол бінарного дерева для візуалізації.

    Зберігає значення вузла, колір та унікальний ідентифікатор,
    який використовується як id вузла в графі.
    """

    def __init__(self, key: int, color: str = "skyblue") -> None:
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
    Додає вузли та ребра бінарного дерева до графа й обчислює координати вузлів.

    :param graph: Орієнтований граф NetworkX, до якого додаються вузли та ребра.
    :param node: Поточний вузол дерева, з якого продовжується побудова.
    :param pos: Словник позицій вузлів у форматі {id: (x, y)}.
    :param x: Поточна координата x для вузла.
    :param y: Поточна координата y для вузла.
    :param layer: Поточний рівень глибини в дереві (корінь = 1).
    :return: Оновлений граф із доданими вузлами та ребрами.
    """
    if node is not None:
        # Додаємо поточний вузол до графа з його кольором і міткою
        graph.add_node(node.id, color=node.color, label=node.val)

        # Додаємо лівого нащадка (якщо існує)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            left_x = x - 1 / 2 ** layer
            pos[node.left.id] = (left_x, y - 1)
            add_edges(graph, node.left, pos, x=left_x, y=y - 1, layer=layer + 1)

        # Додаємо правого нащадка (якщо існує)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            right_x = x + 1 / 2 ** layer
            pos[node.right.id] = (right_x, y - 1)
            add_edges(graph, node.right, pos, x=right_x, y=y - 1, layer=layer + 1)

    return graph


def draw_tree(tree_root: Node) -> None:
    """
    Візуалізує бінарне дерево, починаючи з кореневого вузла.

    Створює орієнтований граф NetworkX, обчислює позиції вузлів
    та відображає дерево за допомогою matplotlib.
    """
    tree = nx.DiGraph()
    pos: Dict[str, Tuple[float, float]] = {tree_root.id: (0.0, 0.0)}

    # Генеруємо граф на основі структури бінарного дерева
    add_edges(tree, tree_root, pos)

    # Отримуємо кольори та мітки вузлів
    colors = [node_data["color"] for _, node_data in tree.nodes(data=True)]
    labels = {node_id: node_data["label"] for node_id, node_data in tree.nodes(data=True)}

    # Малюємо дерево
    plt.figure(figsize=(10, 6))
    nx.draw(
        tree,
        pos=pos,
        labels=labels,
        arrows=False,
        node_size=2500,
        node_color=colors,
    )
    plt.show()


def heap_to_tree(heap: List[int]) -> Optional[Node]:
    """
    Будує бінарне дерево з масиву, що представляє бінарну купу.

    Для елемента з індексом i:
      - індекс лівого нащадка: 2*i + 1
      - індекс правого нащадка: 2*i + 2

    :param heap: Список цілих чисел, що задає бінарну купу.
    :return: Кореневий вузол побудованого дерева або None, якщо купа порожня.
    """
    if not heap:
        return None

    # Створюємо вузол для кожного елемента купи
    nodes: List[Node] = [Node(v) for v in heap]

    # Призначаємо лівих і правих нащадків відповідно до індексів
    for i in range(len(heap)):
        left_i = 2 * i + 1
        right_i = 2 * i + 2

        if left_i < len(heap):
            nodes[i].left = nodes[left_i]
        if right_i < len(heap):
            nodes[i].right = nodes[right_i]

    return nodes[0]


def visualize_heap(heap: List[int]) -> None:
    """
    Візуалізує бінарну купу, задану списком (масивом), у вигляді бінарного дерева.

    Якщо купа порожня, виводить повідомлення й не будує дерево.
    """
    root = heap_to_tree(heap)
    if root is None:
        print("Купа порожня — нічого візуалізувати.")
        return

    draw_tree(root)


if __name__ == "__main__":
    # Приклад: масив, який можна інтерпретувати як мін-купу
    example_heap = [0, 1, 3, 4, 2, 6, 5]
    visualize_heap(example_heap)
