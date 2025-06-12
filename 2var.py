class WordChainGame:
    """
    Строит цепочку слов, где каждое следующее слово начинается
    на букву, на которую заканчивается предыдущее (без учёта 'ь'),
    и последний элемент замыкается на первую букву первого.
    Различает даже одинаковые слова по их позициям.
    """
    def __init__(self, rawInput: str):
        # Разбираем строку: убираем лишние пробелы, оставляем только слова
        self.words = self.splitWords(rawInput)
        if not self.words:
            raise ValueError("Ошибка: не введено ни одного слова.")
        # Граф: ключ — буква, значение — список (целёвая буква, индекс слова)
        self.graph = self.buildGraph()

    def splitWords(self, line: str) -> list[str]:
        """Разбивает входную строку на слова, игнорируя пустые."""
        return [tok for tok in line.strip().split() if tok.isalpha()]

    def getLastLetter(self, word: str) -> str:
        """Возвращает последнюю значимую букву (не считая 'ь')."""
        if word.endswith('ь') and len(word) > 1:
            return word[-2]
        return word[-1]

    def buildGraph(self) -> dict[str, list[tuple[str, int]]]:
        """
        Для каждого слова с индексом i:
          определяет start = word[0], end = getLastLetter(word)
          и кладёт в graph[start].append((end, i))
        """
        graph: dict[str, list[tuple[str, int]]] = {}
        for i, w in enumerate(self.words):
            start = w[0]
            end = self.getLastLetter(w)
            graph.setdefault(start, []).append((end, i))
        return graph

    def searchChain(self,
                    currentIndex: int,
                    usedIndices: set[int],
                    pathIndices: list[int]) -> bool:
        """
        Рекурсивный DFS + бэктрекинг по индексам слов:
          • currentIndex — индекс текущего слова;
          • usedIndices — уже взятые индексы;
          • pathIndices — текущий путь индексов.
        Возвращает True, если найден замкнутый путь длины total_words.
        """
        pathIndices.append(currentIndex)
        usedIndices.add(currentIndex)

        # Если включили все слова — проверяем замыкание
        if len(pathIndices) == len(self.words):
            firstLetter = self.words[pathIndices[0]][0]
            lastLetter = self.getLastLetter(self.words[currentIndex])
            return lastLetter == firstLetter

        # Иначе продолжаем DFS по ребрам из буквы конца currentWord
        nextLetter = self.getLastLetter(self.words[currentIndex])
        for destLetter, nxtIdx in self.graph.get(nextLetter, []):
            if nxtIdx not in usedIndices:
                if self.searchChain(nxtIdx, usedIndices, pathIndices):
                    return True

        # Откат: убираем текущий индекс
        usedIndices.remove(currentIndex)
        pathIndices.pop()
        return False

    def findChain(self) -> list[str] | None:
        """
        Перебираем все слова по индексам в качестве старта.
        Если из какого-то индекса DFS возвращает True — собираем цепочку строк.
        """
        for startIdx in range(len(self.words)):
            used: set[int] = set()
            path: list[int] = []
            if self.searchChain(startIdx, used, path):
                # Возвращаем слова в порядке найденного пути
                return [self.words[i] for i in path]
        return None


def main():
    """
    Читает одну строку со словами через пробел,
    запускает поиск цепочки и выводит результат.
    """
    print("Введите слова через пробелы:")
    raw = input().strip().lower()
    try:
        game = WordChainGame(raw)
        chain = game.findChain()
        if chain:
            print("Найденная цепочка:")
            print(" ".join(chain))
        else:
            print("Цепочку составить невозможно.")
    except ValueError as err:
        print(err)


if __name__ == "__main__":
    main()
