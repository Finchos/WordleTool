import re
import sys
import os

class Solver:
    def __init__(self):

        if hasattr(sys, '_MEIPASS'):
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.path.dirname(__file__)

        answers_path = os.path.join(self.base_path, "answers.txt")
        words_path = os.path.join(self.base_path, "words.txt")

        self.answers = set()

        with open(answers_path, "r", encoding="utf-8") as file:
            self.answers = {line.strip() for line in file}

        self.words = set()

        with open(words_path, "r", encoding="utf-8") as file:
            self.words = {line.strip() for line in file}

        self.alfabet = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}

        self.min_appear = {letter: 0 for letter in self.alfabet}
        self.max_appear = {letter: 5 for letter in self.alfabet}

    def _build_RE(self ,W, S):
        resultRE = "^"
        local_mins = {w: 0 for w in W}

        for w, s in zip(W, S):

            if s == 2:
                resultRE += w
                local_mins[w] += 1

            elif s == 1:
                E = "".join(sorted(self.alfabet - {w}))
                resultRE += f"[{E}]"
                local_mins[w] += 1

            elif s == 0:
                if local_mins[w] > 0:
                    self.max_appear[w] = local_mins[w]
                    E = "".join(sorted(self.alfabet - {w}))
                else:
                    self.alfabet.discard(w)
                    self.max_appear[w] = 0
                    E = "".join(sorted(self.alfabet))
                resultRE += f"[{E}]"

        for w in local_mins:
            if local_mins[w] > self.min_appear[w]:
                self.min_appear[w] = local_mins[w]

        resultRE += "$"
        return resultRE

    def _simulator(self, w, f):
        result = ["."] * 5
        chars = {}

        for char in f:
            if char in chars:
                chars[char] += 1
            else:
                chars[char] = 1

        for i in range(5):
            if w[i] == f[i]:
                result[i] = "2"
                chars[f[i]] -= 1

        for i in range(5):
            if result[i] == ".":
                if chars.get(w[i], 0) > 0:
                    result[i] = "1"
                    chars[w[i]] -= 1
                else:
                    result[i] = "0"
        return "".join(result)

    def process_turn(self, input_word, colours):
        filter = re.compile(self._build_RE(input_word, colours))
        self.answers = {w for w in self.answers if filter.fullmatch(w)}

        valid_answers = set()
        for word in self.answers:
            is_valid = True
            for symbol in self.min_appear:
                count = word.count(symbol)
                if count < self.min_appear[symbol] or count > self.max_appear[symbol]:
                    is_valid = False
                    break
            if is_valid:
                valid_answers.add(word)
        self.answers = valid_answers
        return self.answers

    def pick_optimal_word(self):
        if not self.answers:
            return "NONE"

        optimal_word = ""
        ow_score = 999999

        for w in self.words:
            branches = {}

            for a in self.answers:
                pattern = self._simulator(w, a)

                if pattern not in branches:
                    branches[pattern] = 0
                branches[pattern] += 1

            worst_score = max(branches.values())

            if worst_score < ow_score:
                ow_score = worst_score
                optimal_word = w

            elif worst_score == ow_score:
                if w in self.answers and optimal_word not in self.answers:
                    optimal_word = w

        return optimal_word