from itertools import product, repeat
from itertools import combinations
from multipledispatch import dispatch




def from_normal_to_diagonal(table):
    newtable = [[0 for m in range(16)] for n in range(16)]
    for j in range(16):
        column = [table[i][j] for i in range(16)]
        for i in range(16):
            string_index = shift_index(i, j)
            newtable[string_index][j] = column[i]
    return newtable

def transform(formula, is_sknf_or_sdnf):
    first_operator = 'v' if is_sknf_or_sdnf else '^'
    second_operator = '^' if is_sknf_or_sdnf else 'v'
    formula = formula.replace(first_operator, '').replace(' (', '').replace(') ', '').replace('(', '').replace(')', '')
    sts = formula.split(second_operator)
    buffer = []
    for st in sts:
        st = st.split('  ')
        buffer.append(st)
    sts = buffer
    return sts

def shift_index(index, shift_number):
    newindex = shift_number + index
    if newindex >= 16:
        return newindex - 16
    else:
        return newindex

@dispatch(str, bool, list)
def calculation_method(formula, is_sknf_or_sdnf, sts):
    first_operator = 'v' if is_sknf_or_sdnf else '^'
    second_operator = '^' if is_sknf_or_sdnf else 'v'

    output = []

    for st in sts:
        checker = 0
        for st2 in sts:
            if st != st2:
                logic_sum = (list(set(st) & set(st2)))
                if len(logic_sum) == len(st) - 1:
                    if (str(list(set(st) - set(logic_sum))[0]) == '-' + str(
                            list(set(st2) - set(logic_sum))[0])) or (
                            str(list(set(st2) - set(logic_sum))[0]) == '-' + str(
                        list(set(st) - set(logic_sum))[0])):
                        output.append(logic_sum)
                    else:
                        checker += 1
                else:
                    checker += 1
        if checker == len(sts) - 1:
            output.append(st)
    buffer = []
    for obj in buffer:
        obj = obj.sort()
    [buffer.append(x) for x in output if x not in buffer]
    buffer = sorted(buffer, key=len)


    output = ''
    if len(buffer) == 1 and len(buffer[0]) == 1:
        output = buffer[0][0]
    else:
        for obj in buffer:
            if len(obj) == 1:
                output = output + obj[0] + second_operator
            else:
                output = output + '('
                for item in obj:
                    output = output + item + ' ' + first_operator + ' '
                output = output[:-3] + ') ' + second_operator + ' '
        if output[-3:] == ' v ' or output[-3:] == ' ^ ':
            output = output[:-3]
        else:
            output = output[:-1]

    return output

def add_new_word(word, standart_table, diagonal_table):
    empty_index = 0
    while standart_table[empty_index] != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
        empty_index += 1
    standart_table[empty_index] = [word[i] for i in range(16)]
    for j in range(16):
        string_index = shift_index(empty_index, j)
        diagonal_table[string_index][j] = word[j]

@dispatch(str, bool)
def calculation_method(formula, is_sknf_or_sdnf):
    first_operator = 'v' if is_sknf_or_sdnf else '^'
    second_operator = '^' if is_sknf_or_sdnf else 'v'

    sts = transform(formula, is_sknf_or_sdnf)

    output = []

    for st in sts:
        checker = 0
        for st2 in sts:
            if st != st2:
                logic_sum = (list(set(st) & set(st2)))
                if len(logic_sum) == len(st) - 1:
                    if (str(list(set(st) - set(logic_sum))[0]) == '-' + str(
                            list(set(st2) - set(logic_sum))[0])) or (
                            str(list(set(st2) - set(logic_sum))[0]) == '-' + str(
                            list(set(st) - set(logic_sum))[0])):
                        output.append(logic_sum)
                    else:
                        checker += 1
                else:
                    checker += 1
        if checker == len(sts) - 1:
            output.append(st)
    buffer = []
    for obj in buffer:
        obj = obj.sort()
    [buffer.append(x) for x in output if x not in buffer]
    buffer = sorted(buffer, key=len)

    # print(buffer)
    # print('------------------------------------')

    output = ''
    if len(buffer) == 1 and len(buffer[0]) == 1:
        output = buffer[0][0]
    else:
        for obj in buffer:
            if len(obj) == 1:
                output = output + obj[0] + second_operator
            else:
                output = output + '('
                for item in obj:
                    output = output + item + ' ' + first_operator + ' '
                output = output[:-3] + ') ' + second_operator + ' '
        if output[-3:] == ' v ' or output[-3:] == ' ^ ':
            output = output[:-3]
        else:
            output = output[:-1]

    return output

def read_column(table, index):
    return [table[shift_index(index, i)][i] for i in range(16)]

def calculation_method_str(formula, is_sknf_or_sdnf, counter):
    result = calculation_method(formula, is_sknf_or_sdnf)
    if is_sknf_or_sdnf:
        for i in range(0, counter - 2):
            result = calculation_method(result, is_sknf_or_sdnf)
    else:
        for i in range(0, counter - 2):
            result = calculation_method(result, is_sknf_or_sdnf)
    return result

def sum(table, standart_table, V):
    for i in range(16):
        word = read_column(table, i)
        if [word[0], word[1], word[2]] == V:
            A, B = [], []
            S = [0, 0, 0, 0, 0]
            for j in range(4):
                A.append(word[3 + j])
                B.append(word[7 + j])
            for j in range(4):
                S[len(S) - j - 1] += A[len(A) - j - 1] + B[len(B) - j - 1]
                if S[len(S) - j - 1] >= 2:
                    S[len(S) - j - 1] -= 2
                    S[len(S) - j - 2] = 1
            for j in range(11, 16):
                string_index = shift_index(i, j)
                table[string_index][j] = S[j - 11]
            standart_table[i] = read_column(table, i)

def check(table):
    checker = ['X'] * len(table[0])
    for_check = [''] * len(table[0])
    for obj in table:
        for index, item in enumerate(obj):
            if item == 'X' and for_check[index] == '':
                for_check[index] = 'X'
    return checker == for_check

def f1(first_word, second_word, standart_table, diagonal_table):
    rezult = []
    for i in range(len(first_word)):
        if first_word[i] == 1 and second_word[i] == 1:
            rezult.append(1)
        else:
            rezult.append(0)
    add_new_word(rezult, standart_table, diagonal_table)

def kvain_mac_clascki(table):
    result = []
    for amount in range(1, len(table) - 1):
        buffer = combinations(table, amount)
        for obj in buffer:
            if check(obj):
                result.append(obj)
        if len(result) != 0:
            return result

def f14(first_word, second_word, standart_table, diagonal_table):
    rezult = []
    for i in range(len(first_word)):
        if not (first_word[i] == 1 and second_word[i] == 1):
            rezult.append(1)
        else:
            rezult.append(0)
    add_new_word(rezult, standart_table, diagonal_table)

def calculation_tabular_method(formula, is_sknf_or_sdnf, counter):
    main_formula = transform(formula, is_sknf_or_sdnf)
    tupic_formula = transform(calculation_method(formula, is_sknf_or_sdnf), is_sknf_or_sdnf)
    table = []
    # Постройка таблицы
    for item in tupic_formula:
        buffer = []
        for obj in main_formula:
            buffer.append('X') if set(item).issubset(obj) else buffer.append(' ')
        table.append(buffer)

    # Число для отступов
    print_number = counter * 2 + (counter - 1) * 4 + 2
    # Вывод таблицы
    print((' ' * print_number) + formula)
    for i in range(0, len(tupic_formula)):
        print(f"%{print_number - 2}s" % tupic_formula[i], end='   ')
        for j in range(0, len(table[i])):
            print(str(table[i][j]).center(print_number - 3, '-'), end='')
        print('\n')

    # Устранение лишних импликант
    result = kvain_mac_clascki(table)

    outputs = []

    if result != None:
        for index_of_options in range(0, len(result)):
            buffer_tupic_formula = []
            for index in range(0, len(table)):
                if not table[index] in result[index_of_options]:
                    buffer_tupic_formula.append(tupic_formula[index])

            result_table = result[index_of_options]

            # Вывод таблицы
            # print((' ' * print_number) + formula)
            # for i in range(0, len(buffer_tupic_formula)):
            #     print(f"%{print_number - 2}s" % buffer_tupic_formula[i], end='   ')
            #     for j in range(0, len(result_table[i])):
            #         print(str(result_table[i][j]).center(print_number - 3, '-'), end='')
            #     print('\n')

            output = calculation_method('', is_sknf_or_sdnf, buffer_tupic_formula)
            outputs.append(output)
        print(calculation_method(calculation_method(formula, is_sknf_or_sdnf), is_sknf_or_sdnf))
    else:
        print(calculation_method(formula, is_sknf_or_sdnf))

def f3(first_word, standart_table, diagonal_table):
    add_new_word(first_word, standart_table, diagonal_table)

def method_carno(table, vars, formula, is_sknf_or_sdnf, amount):
    result = []
    counter = 0
    for i in range(1, 3):
        buffer = []
        while counter < len(table) / 2 * i:
            if len(table) / 2 * i - counter == 2:
                buffer.append(table[counter + 1])
            else:
                if len(table) / 2 * i - counter == 1:
                    buffer.append(table[counter - 1])
                else:
                    buffer.append(table[counter])
            counter += 1
        result.append(buffer)

    print(
        '     !' + vars[1] + ' !' + vars[2] + '   !' + vars[1] + ' ' + vars[2] + '    ' + vars[1] + ' ' + vars[
            2] + '    ' + vars[1] + ' !' + vars[2])
    print('!' + vars[0] + '   ' + str(result[0]))
    print(' ' + vars[0] + '   ' + str(result[1]))
    print(calculation_method_str(formula, is_sknf_or_sdnf, amount))

def f12(first_word, standart_table, diagonal_table):
    rezult = []
    for i in range(len(first_word)):
        if first_word[i] == 1:
            rezult.append(1)
        else:
            rezult.append(0)
    add_new_word(rezult, standart_table, diagonal_table)

def checkPrime(n):
    if n == 1 or n == 0:
        return 0

    for i in range(2, n//2):
        if n % i == 0:
            return 0
    return 1

def compare(first_word, second_word):
    g = 0
    l = 0

    word_first = [bool(first_word[i]) for i in range(len(first_word))]
    word_second = [bool(second_word[i]) for i in range(len(second_word))]

    for i in range(len(first_word)):
        g = g or (not (word_second[i]) and word_first[i] and not (l))
        l = l or (word_second[i] and not (word_first[i]) and not (g))

    if g == 0 and l == 0:
        return '='
    elif g == 1 and l == 0:
        return '>'
    else:
        return '<'

def getPrime(n):
    if n % 2 == 0:
        n = n + 1
    while not checkPrime(n):
        n += 2
    return n

def most_big(mas_word):
    if mas_word == []:
        return None
    copy_mas = mas_word.copy()
    for i in range(len(copy_mas[0])):
        biggest_word = []
        for j in range(len(copy_mas)):
            if copy_mas[j][i] == 1:
                biggest_word.append(copy_mas[j])
        if biggest_word != []:
            copy_mas = biggest_word

    return copy_mas

def hashFunction(key):
    capacity = getPrime(10)
    return key % capacity

def most_little(mas_word):
    if mas_word == []:
        return None
    copy_mas = mas_word.copy()
    for i in range(len(copy_mas[0])):
        smallest_word = []
        for j in range(len(copy_mas)):
            if copy_mas[j][i] == 0:
                smallest_word.append(copy_mas[j])
        if smallest_word != []:
            copy_mas = smallest_word

    return copy_mas
hashTable = [[],] * 10
def insertData(key, data):
    index = hashFunction(key)
    hashTable[index] = [key, data]

def find_down(mas_word, key_word):
    smaller_word = []
    for i in range((len(mas_word))):
        if compare(key_word, mas_word[i]) == '>':
            smaller_word.append(mas_word[i])

    biggest = most_big(smaller_word)
    return biggest

def removeData(key):
    index = hashFunction(key)
    hashTable[index] = 0

class hash():
    __SIZE = 20

    def __init__(self):
        self.header = ['№', 'Next', 'Prev', 'Hash', 'Index', 'Key', 'Value']
        self.table = []
        for index in range(self.__SIZE):
            stroka = []
            for j in range(len(self.header)):
                stroka.append('')
            stroka[0] = index
            self.table.append(stroka)

    def get_hash_address(self, key: int):
        return key % self.__SIZE

    def get_alphabet_pos(self, example: str):
        return ord(example.upper()) - 65

    def get_vh(self, key: str):
        a = self.get_alphabet_pos(key[0])
        b = self.get_alphabet_pos(key[1])
        V = a * 26 + b
        return V, self.get_hash_address(V)

    def get_value(self, key: str):
        key = self.get_v(key)
        return self.table[key]

    def add_value(self, key: str, value: str):
        v, h = self.get_vh(key)
        if self.table[h][1] == '':
            self.save(key, value, h, v, h, 'no')
        else:
            self.find_no(v, h, key, value)

    def find_no(self, v, h, key, value):
        next = h
        prev = h
        if self.table[next][4] == h:
            while self.table[next][1] != 'no':
                next = self.table[next][1]
            if self.table[next][1] == 'no':
                prev = next
                address = self.find_place_in_table(next)
            if address != None:
                self.table[next][1] = address
                self.save(key, value, h, v, address, prev)
        else:
            address = self.find_place(next)
            if address != None:
                self.save(key, value, h, v, address, 'no')

    def find_place_in_table(self, next):
        begin_address = self.table[next][0]
        address = begin_address + 1
        if address >= self.__SIZE - 1: address = 0
        while self.table[address][1] != '' and address != begin_address:
            if address >= self.__SIZE - 1:
                address = 0
            else:
                address += 1
        if address != begin_address:
            return address
        else:
            return None

    def save(self, key, value, h, v, address, prev):
        self.table[address][3] = v
        self.table[address][4] = h
        self.table[address][5] = key
        self.table[address][6] = value
        self.table[address][1] = 'no'
        self.table[address][2] = prev
        self.table[address][0] = address

    def print(self):
        print('________________________TABLE______________________')
        line = [str(self.header[i]) for i in range(len(self.header))]
        line = '\t'.join(line)
        print(line)
        for i in range(len(self.table)):
            line = [str(self.table[i][j]) for j in range(len(self.table[i]))]
            line = '\t'.join(line)
            print(line)

    def search(self, key):
        v, h = self.get_vh(key)
        if self.table[h][5] != key:
            while self.table[h][5] != key:
                if self.table[h][1] == 'no': break
                h = self.table[h][1]
        if self.table[h][5] == key:
            return self.table[h]
        else:
            return None

    def delete(self, key):
        line = self.search(key)
        if line == None: return
        index = line[0]
        next = line[1]
        prev = line[2]
        if prev == 'no' and next != 'no': self.table[next][2] = 'no'
        if prev != 'no' and next == 'no': self.table[prev][1] = 'no'
        if prev != 'no' and next != 'no':
            self.table[prev][1] = next
            self.table[next][2] = prev
        for i in range(len(self.table[index]) - 1):
            self.table[index][i + 1] = ''

def find_up(mas_word, key_word):
    bigger_word = []
    for i in range((len(mas_word))):
        if compare(key_word, mas_word[i]) == '<':
            bigger_word.append(mas_word[i])

    smallest = most_little(bigger_word)
    return smallest


standart_table = [[0 for i in range(16)] for j in range(16)]
diagonal_table = from_normal_to_diagonal(standart_table)
while True:
    operation = input(
        '\n 1 - Добавить новое слово \n 2 - Сложение \n 3 - Чтение столбца \n 4 - Функция f1 \n 5 - Функция f14 \n 6 - Функция f3 \n 7 - Функция f12\n' +
        ' 8 - Поиск ближайшего снизу значения \n 9 - Поиск ближайшего сверху значения \n 10 - Показать таблицы \n')
    if operation == '1':
        word = input('Введите слово: ')
        word = word.replace(' ', '')
        word = [int(word[i]) for i in range(16)]
        add_new_word(word, standart_table, diagonal_table)
    elif operation == '2':
        V = input('Введите V: ')
        V = V.replace(' ', '')
        V = [int(V[i]) for i in range(len(V))]
        sum(diagonal_table, standart_table, V)
    elif operation == '3':
        index = int(input('Введите индекс столбца: '))
        print(read_column(diagonal_table, index))
    elif operation == '4':
        first_word_index = int(input('Введите индекс первого слова: '))
        second_word_index = int(input('Введите индекс второго слова: '))
        first_word = read_column(diagonal_table, first_word_index)
        second_word = read_column(diagonal_table, second_word_index)
        f1(first_word, second_word, standart_table, diagonal_table)
    elif operation == '5':
        first_word_index = int(input('Введите индекс первого слова: '))
        second_word_index = int(input('Введите индекс второго слова: '))
        first_word = read_column(diagonal_table, first_word_index)
        second_word = read_column(diagonal_table, second_word_index)
        f14(first_word, second_word, standart_table, diagonal_table)
    elif operation == '6':
        first_word_index = int(input('Введите индекс первого слова: '))
        second_word_index = int(input('Введите индекс второго слова: '))
        first_word = read_column(diagonal_table, first_word_index)
        f3(first_word, standart_table, diagonal_table)
    elif operation == '7':
        first_word_index = int(input('Введите индекс первого слова: '))
        second_word_index = int(input('Введите индекс второго слова: '))
        first_word = read_column(diagonal_table, first_word_index)
        f12(first_word, standart_table, diagonal_table)
    elif operation == '8':
        word = input('Введите свое слово: ')
        word = word.replace(' ', '')
        word = [int(word[i]) for i in range(16)]
        smallest = find_down(standart_table, word)
        if smallest == None:
            print('Нет слова меньше заданного!')
        else:
            for word in smallest:
                print(word)
    elif operation == '9':
        word = input('Введите свое слово: ')
        word = word.replace(' ', '')
        word = [int(word[i]) for i in range(16)]
        biggest = find_up(standart_table, word)
        if biggest == None:
            print('Нет слова больше заданного!')
        else:
            for word in biggest:
                print(word)
    elif operation == '10':
        print('\nОбычная таблица:')
        for i in range(16):
            print(standart_table[i])
        print('\nДиагональная таблица:')
        for i in range(16):
            print(diagonal_table[i])