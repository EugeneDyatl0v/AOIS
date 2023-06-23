from random import randint


class Processor:
    def __init__(self, word_size, size, data=None):
        if data:
            self.data = data
        else:
            self.data = ["".join([str(randint(0, 1)) for _ in range(word_size)]) for _ in range(size)]

    def search(self, search_str):
        max_match = 0
        match_indices = []

        for i, item in enumerate(self.data):
            match_count = 0

            for j in range(len(search_str)):
                if search_str[j] == item[j]:
                    match_count += 1

            if match_count > max_match:
                max_match = match_count
                match_indices = [i]
            elif match_count == max_match:
                match_indices.append(i)

        return [self.data[i] for i in match_indices]

    size_of_table = 16
    FOUR = 4
    A_start = 3
    B_start = 7
    S_start = 11

    def from_normal_to_diagonal(table):
        newtable = [[0 for m in range(size_of_table)] for n in range(size_of_table)]
        for j in range(size_of_table):
            column = [table[i][j] for i in range(size_of_table)]
            for i in range(size_of_table):
                string_index = shift_index(i, j)
                newtable[string_index][j] = column[i]
        return newtable

    def shift_index(index, shift_number):
        newindex = shift_number + index
        if newindex >= size_of_table:
            return newindex - size_of_table
        else:
            return newindex

    def add_new_word(word, standart_table, diagonal_table):
        empty_index = 0
        while standart_table[empty_index] != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
            empty_index += 1
        standart_table[empty_index] = [word[i] for i in range(size_of_table)]
        for j in range(size_of_table):
            string_index = shift_index(empty_index, j)
            diagonal_table[string_index][j] = word[j]

    def read_column(table, index):
        return [table[shift_index(index, i)][i] for i in range(size_of_table)]

    def sum(table, standart_table, V):
        for i in range(size_of_table):
            word = read_column(table, i)
            if [word[0], word[1], word[2]] == V:
                A, B = [], []
                S = [0, 0, 0, 0, 0]
                for j in range(FOUR):
                    A.append(word[A_start + j])
                    B.append(word[B_start + j])
                for j in range(FOUR):
                    S[len(S) - j - 1] += A[len(A) - j - 1] + B[len(B) - j - 1]
                    if S[len(S) - j - 1] >= 2:
                        S[len(S) - j - 1] -= 2
                        S[len(S) - j - 2] = 1
                for j in range(S_start, size_of_table):
                    string_index = shift_index(i, j)
                    table[string_index][j] = S[j - S_start]
                standart_table[i] = read_column(table, i)

    def f1(first_word, second_word, standart_table, diagonal_table):
        rezult = []
        for i in range(len(first_word)):
            if first_word[i] == 1 and second_word[i] == 1:
                rezult.append(1)
            else:
                rezult.append(0)
        add_new_word(rezult, standart_table, diagonal_table)

    def f14(first_word, second_word, standart_table, diagonal_table):
        rezult = []
        for i in range(len(first_word)):
            if not (first_word[i] == 1 and second_word[i] == 1):
                rezult.append(1)
            else:
                rezult.append(0)
        add_new_word(rezult, standart_table, diagonal_table)

    def f3(first_word, standart_table, diagonal_table):
        add_new_word(first_word, standart_table, diagonal_table)

    def f12(first_word, standart_table, diagonal_table):
        rezult = []
        for i in range(len(first_word)):
            if first_word[i] == 1:
                rezult.append(1)
            else:
                rezult.append(0)
        add_new_word(rezult, standart_table, diagonal_table)

    def g_l_trigger(self, first_word :str, second_word :str):
        g = False
        l = False
        for i in range(0, len(first_word)):
            if g or (first_word[i] == '1' and second_word[i] == '0' and not l):
                g = True
            else:
                g = False
            if l or (first_word[i] == '0' and second_word[i] == '1' and not g):
                l = True
            else:
                l = False
        if g:
            return True
        if l:
            return False
        return False

    def interval_find(self, min_check :str, max_check :str):
        more_than_min = []
        final_list = []
        for word in self.data:
            if self.g_l_trigger(word, min_check):
                more_than_min.append(word)
        for word in more_than_min:
            if not self.g_l_trigger(word, max_check) and word != max_check:
                final_list.append(word)
        return final_list


if __name__ == '__main__':
    processor = Processor(3, 10)
    print(processor.data)
    print(processor.g_l_trigger('011', '100'))
    print(f'Поиск по соответствию: {processor.search("111")}')
    print(f'Поиск по соответствию: {processor.search("101")}')
    print(f'Поиск по соответствию: {processor.search("000")}')
    print(f'Поиск по соответствию: {processor.search("1x0")}')

    print(f'Поиск в интервале: {processor.interval_find("010", "101")}')