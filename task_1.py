"""
Реалізація однозвʼязного списку на Python для навчальних цілей.

Містить:
- клас Node для вузла списку;
- клас LinkedList з операціями вставки, пошуку, видалення та друку;
- метод reverse() для реверсування списку in-place;
- реалізацію сортування однозвʼязного списку за допомогою merge sort;
- статичний метод merge_two_sorted_lists() для обʼєднання двох відсортованих
  однозвʼязних списків в один відсортований список без копіювання вузлів.
"""

from typing import Optional, Tuple


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next: Optional["Node"] = None


class LinkedList:
    def __init__(self):
        self.head: Optional[Node] = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def insert_after(self, prev_node: Node, data):
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int):
        """Видаляє перший вузол із значенням key зі списку, якщо він існує."""
        cur = self.head

        # Обробляємо випадок, коли видаляємо голову
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return

        prev = None
        # Шукаємо вузол із даними key
        while cur and cur.data != key:
            prev = cur
            cur = cur.next

        # Перериваємося, якщо вузол не знайдено
        if cur is None:
            return

        # Вирізаємо вузол із ланцюжка
        prev.next = cur.next
        cur = None

    def search_element(self, data: int) -> Optional[Node]:
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def print_list(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

    def reverse(self) -> None:
        """Реверсує список in-place, змінюючи посилання next."""
        prev = None
        curr = self.head

        while curr:
            nxt = curr.next      # Зберігаємо посилання на наступний вузол
            curr.next = prev     # Розвертаємо посилання next
            prev = curr          # Зсуваємо prev уперед
            curr = nxt           # Зсуваємо curr уперед

        self.head = prev         # Оновлюємо голову списку

    def _split(self, head: Node) -> Tuple[Optional[Node], Optional[Node]]:
        """Повертає кортеж (ліва_половина, права_половина) для списку з головою head."""
        if head is None or head.next is None:
            return head, None

        slow = head
        fast = head.next

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        middle = slow.next
        slow.next = None
        return head, middle

    def _merge_sorted(self, a: Optional[Node], b: Optional[Node]) -> Optional[Node]:
        """Зливає два відсортовані списки (вузли a і b) у один відсортований."""
        if a is None:
            return b
        if b is None:
            return a

        if a.data <= b.data:
            result = a
            result.next = self._merge_sorted(a.next, b)
        else:
            result = b
            result.next = self._merge_sorted(a, b.next)
        return result

    def _merge_sort(self, head: Optional[Node]) -> Optional[Node]:
        """Застосовує рекурсивний merge sort до списку з головою head."""
        if head is None or head.next is None:
            return head

        left, right = self._split(head)
        left_sorted = self._merge_sort(left)
        right_sorted = self._merge_sort(right)
        return self._merge_sorted(left_sorted, right_sorted)

    def sort(self) -> None:
        """Сортує поточний список in-place, змінюючи посилання next."""
        self.head = self._merge_sort(self.head)

    @staticmethod
    def merge_two_sorted_lists(l1: "LinkedList", l2: "LinkedList") -> "LinkedList":
        """
        Обʼєднує два відсортовані однозвʼязні списки в один відсортований.

        Передбачається, що l1 і l2 вже відсортовані за неспаданням.
        Вузли не копіюються: перевикористовуються існуючі, змінюються лише посилання next.
        """
        prehead = Node(0)
        tail = prehead

        a = l1.head
        b = l2.head

        while a and b:
            if a.data <= b.data:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next

        # Додаємо решту елементів з того списку, де вони залишилися
        tail.next = a if a is not None else b

        merged = LinkedList()
        merged.head = prehead.next
        return merged


if __name__ == "__main__":
    # Невелика перевірка усіх трьох вимог завдання

    l1 = LinkedList()
    l1.insert_at_end(3)
    l1.insert_at_end(1)
    l1.insert_at_end(5)

    l2 = LinkedList()
    l2.insert_at_end(2)
    l2.insert_at_end(4)
    l2.insert_at_end(6)

    print("l1 до сортування:")
    l1.print_list()
    l1.sort()
    print("l1 після сортування:")
    l1.print_list()

    print("l2 до реверсу:")
    l2.print_list()
    l2.reverse()
    print("l2 після реверсу:")
    l2.print_list()
    l2.reverse()  # Повертаємо l2 до сортування за зростанням перед злиттям

    merged = LinkedList.merge_two_sorted_lists(l1, l2)
    print("Результат злиття двох відсортованих списків:")
    merged.print_list()
