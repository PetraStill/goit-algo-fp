"""
Модуль реалізує зважений граф та алгоритм Дейкстри з використанням бінарної купи.
Функціональність модуля включає:
- створення графа зі списками суміжності;
- додавання вершин і ребер з вагами;
- знаходження найкоротших шляхів від початкової вершини до всіх інших
  за допомогою алгоритму Дейкстри (черга з пріоритетами через heapq);
- відновлення повного маршруту до заданої цільової вершини;
- побудову тестового транспортного графа;
- консольну взаємодію з користувачем для пошуку найкоротшого маршруту.
"""

from __future__ import annotations
from typing import Dict, List, Tuple, Optional
import heapq


class Graph:
    """
    Клас для представлення зваженого графа у вигляді списків суміжності.
    Дозволяє додавати вершини та ребра з вагами.
    """

    def __init__(self) -> None:
        # Ініціалізуємо словник: вершина → список суміжних (вершина, вага)
        self.adj: Dict[str, List[Tuple[str, float]]] = {}

    def add_vertex(self, v: str) -> None:
        """Додаємо вершину до графа, якщо вона ще не існує."""
        if v not in self.adj:
            self.adj[v] = []  # Ініціалізуємо пустий список суміжних вершин

    def add_edge(self, u: str, v: str, weight: float, undirected: bool = False) -> None:
        """
        Додаємо ребро між u → v з указаною вагою.
        Якщо undirected=True — додаємо обидва напрямки.
        """
        self.add_vertex(u)  # Гарантуємо, що вершина існує
        self.add_vertex(v)

        # Додаємо напрямок u → v
        self.adj[u].append((v, weight))

        # Додаємо напрямок v → u, якщо граф неорієнтований
        if undirected:
            self.adj[v].append((u, weight))


def dijkstra_with_paths(
    graph: Graph,
    start: str,
) -> tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Алгоритм Дейкстри з використанням бінарної купи.
    Повертає словник мінімальних відстаней та словник попередників для побудови шляхів.
    """

    # Ініціалізуємо всі відстані нескінченністю
    dist: Dict[str, float] = {v: float("inf") for v in graph.adj}

    # Ініціалізуємо попередників None
    prev: Dict[str, Optional[str]] = {v: None for v in graph.adj}

    # Встановлюємо початкову вершину з нульовою відстанню
    dist[start] = 0.0

    # Ініціалізуємо бінарну купу (мін-heap)
    heap: List[Tuple[float, str]] = [(0.0, start)]

    while heap:
        # Дістаємо вершину з найменшою відстанню
        current_dist, u = heapq.heappop(heap)

        # Пропускаємо застарілі значення у купі
        if current_dist > dist[u]:
            continue

        # Перебираємо всіх сусідів вершини u
        for v, weight in graph.adj[u]:
            # Рахуємо нову потенційну відстань до v
            new_dist = current_dist + weight

            # Перевіряємо, чи можна покращити шлях
            if new_dist < dist[v]:
                dist[v] = new_dist           # Оновлюємо відстань
                prev[v] = u                  # Оновлюємо попередника
                # Додаємо у купу новий шлях
                heapq.heappush(heap, (new_dist, v))

    return dist, prev


def reconstruct_path(
    prev: Dict[str, Optional[str]],
    start: str,
    target: str,
) -> List[str]:
    """
    Відновлює маршрут від start до target, використовуючи словник попередників.
    Повертає шлях як список вершин або порожній список, якщо шляху немає.
    """

    # Обробляємо випадок, коли старт і ціль збігаються
    if start == target:
        return [start]

    # Якщо попередника немає — шляху не існує
    if prev[target] is None:
        return []

    path: List[str] = []
    cur: Optional[str] = target

    # Підіймаємося по ланцюжку попередників
    while cur is not None:
        path.append(cur)       # Додаємо вершину до шляху
        if cur == start:
            break
        cur = prev[cur]        # Переходимо до попередньої вершини

    # Перевіряємо, чи шлях дійсно доходить до start
    if path[-1] != start:
        return []

    # Розвертаємо шлях у правильний порядок
    path.reverse()
    return path


def build_transport_graph() -> Graph:
    """
    Створює приклад зваженого транспортного графа.
    Використовує неорієнтовані ребра з вагами (час у хвилинах).
    """
    g = Graph()

    g.add_edge("Dworzec Glowny", "Rynek", 10, undirected=True)
    g.add_edge("Dworzec Glowny", "Galeria Dominikanska", 5, undirected=True)
    g.add_edge("Galeria Dominikanska", "Rynek", 4, undirected=True)
    g.add_edge("Rynek", "Ostrów Tumski", 7, undirected=True)
    g.add_edge("Galeria Dominikanska", "Ostrów Tumski", 6, undirected=True)

    return g


def main() -> None:
    """
    Основна функція програми:
    – виводить доступні вершини;
    – зчитує старт і ціль;
    – запускає алгоритм Дейкстри;
    – відновлює та виводить найкоротший шлях.
    """

    g = build_transport_graph()

    print("Доступні зупинки:")
    # Виводимо всі вершини у відсортованому порядку
    for v in sorted(g.adj.keys()):
        print(" -", v)

    # Зчитуємо початкову та кінцеву зупинку
    start = input("\nПочаткова зупинка: ").strip()
    target = input("Кінцева зупинка: ").strip()

    # Перевіряємо, що обидві зупинки існують у графі
    if start not in g.adj or target not in g.adj:
        print("Одна з вказаних зупинок відсутня в графі.")
        return

    # Викликаємо алгоритм Дейкстри
    dist, prev = dijkstra_with_paths(g, start)

    # Відновлюємо маршрут
    path = reconstruct_path(prev, start, target)

    # Перевіряємо, чи існує шлях
    if not path or dist[target] == float("inf"):
        print(f"Маршрут з '{start}' до '{target}' відсутній.")
    else:
        path_str = " -> ".join(path)
        print(f"\nНайшвидший маршрут: {path_str}")
        print(f"Час у дорозі: {dist[target]:.0f} хв")


if __name__ == "__main__":
    main()
