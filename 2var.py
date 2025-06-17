class WordChainGame:
    def __init__(self, raw_input: str):
        self.words = [w for w in raw_input.strip().split() if w.isalpha()]
        if not self.words:
            raise ValueError("не введено ни одного слова.")
        self.graph = self.build_graph()

    def get_last_letter(self, word: str) -> str:
        return word[-2] if word.endswith('ь') and len(word) > 1 else word[-1]

    def build_graph(self) -> dict[str, list[int]]:
        graph: dict[str, list[int]] = {}
        for i, word in enumerate(self.words):
            start = word[0]
            graph.setdefault(start, []).append(i)
        return graph

    def dfs(self, index: int, path: list[int], used: set[int]) -> bool:
        path.append(index)
        used.add(index)

        if len(path) == len(self.words):
            return self.get_last_letter(self.words[path[-1]]) == self.words[path[0]][0]

        next_letter = self.get_last_letter(self.words[index])
        for i in self.graph.get(next_letter, []):
            if i not in used:
                if self.dfs(i, path, used):
                    return True

        path.pop()
        used.remove(index)
        return False

    def find_chain(self) -> list[str] | None:
        for i in range(len(self.words)):
            path, used = [], set()
            if self.dfs(i, path, used):
                return [self.words[j] for j in path]
        return None

def main():
    print("Введите слова через пробелы:")
    try:
        raw = input().strip().lower()
        if not raw:
            raise ValueError("Ввод пуст.")

        game = WordChainGame(raw)
        chain = game.find_chain()

        if chain:
            print("Найденная цепочка:")
            print(" ".join(chain))
        else:
            print("Цепочку составить невозможно.")

    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
