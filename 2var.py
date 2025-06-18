class Stack:
    class Node:
        def __init__(self, value, next=None):
            self.value = value
            self.next = next

    def __init__(self):
        self.head = None
        self.size = 0

    def push(self, value):
        self.head = self.Node(value, self.head)
        self.size += 1

    def pop(self):
        if self.head is None:
            raise ValueError("Стек пуст")
        value = self.head.value
        self.head = self.head.next
        self.size -= 1
        return value

    def top(self):
        if self.head is None:
            raise ValueError("Стек пуст")
        return self.head.value

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result[::-1]  # Перевернуть, так как стек - LIFO

    def __len__(self):
        return self.size


class Set:
    class Node:
        def __init__(self, value, next=None):
            self.value = value
            self.next = next

    def __init__(self):
        self.head = None
        self.size = 0

    def add(self, value):
        if self.contains(value):
            return
        self.head = self.Node(value, self.head)
        self.size += 1

    def remove(self, value):
        prev = None
        curr = self.head
        while curr:
            if curr.value == value:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                self.size -= 1
                return
            prev = curr
            curr = curr.next

    def contains(self, value):
        curr = self.head
        while curr:
            if curr.value == value:
                return True
            curr = curr.next
        return False

    def __len__(self):
        return self.size


class WordChainGame:
    def __init__(self, raw_input):
        self.words = [w for w in raw_input.strip().split() if w.isalpha()]
        if not self.words:
            raise ValueError("не введено ни одного слова.")
        self.graph = self.build_graph()

    def last_letter(self, word):
        # Если слово заканчивается мягким знаком 'ь', берем предпоследнюю букву
        return word[-2] if word.endswith('ь') and len(word) > 1 else word[-1]

    def build_graph(self):
        graph = {}
        for i, word in enumerate(self.words):
            graph.setdefault(word[0], []).append(i)
        return graph

    def dfs(self, index, path, used):
        path.push(index)
        used.add(index)

        if len(path) == len(self.words):
            # Проверяем замкнутость цепочки: последняя буква последнего слова == первая буква первого слова
            last_char = self.last_letter(self.words[path.top()])
            first_char = self.words[path.to_list()[0]][0]
            if last_char == first_char:
                return True

        next_letter = self.last_letter(self.words[index])
        for i in self.graph.get(next_letter, []):
            if not used.contains(i):
                if self.dfs(i, path, used):
                    return True

        path.pop()
        used.remove(index)
        return False

    def find_chain(self):
        for i in range(len(self.words)):
            path, used = Stack(), Set()
            if self.dfs(i, path, used):
                return [self.words[j] for j in path.to_list()]
        return None


def main():
    print("Добро пожаловать в игру 'Цепочка слов'!")
    print("Введите список слов через пробел.")
    print("Все слова должны быть на русском языке, состоять только из букв.")
    print("Пример ввода: зонт ток корова арбуз")
    print()

    try:
        raw = input("Ваш ввод: ").strip().lower()
        if not raw:
            raise ValueError("Ввод пуст. Пожалуйста, введите хотя бы одно слово.")
        game = WordChainGame(raw)
        chain = game.find_chain()
        if chain:
            print("\nНайдена цепочка:")
            print(" → ".join(chain))
        else:
            print("\nЦепочку составить невозможно.")
    except ValueError as err:
        print(f"\nОшибка: {err}")


if __name__ == "__main__":
    main()
