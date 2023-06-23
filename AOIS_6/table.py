from itertools import product, repeat
from itertools import combinations
from multipledispatch import dispatch
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




class AOIS_6:
    table = []
    result_of_table = []
    vars = []

    def translate(self, args, logic):
        result = logic.replace('v', ' or ').replace('^', ' and ').replace('-', ' not ')
        for index in range(0, len(self.vars)):
            result = result.replace(str(self.vars[index]), str(args[index]))
            # print(result)
        return result

    def truthtable(self, logic_formula):
        operators = ['(', ')', 'v', '^', '-', ' ']

        for index in range(0, len(logic_formula)):
            if logic_formula[index] not in operators:
                self.vars.append(logic_formula[index])
        self.vars = list(set(self.vars))
        self.vars.sort()

        print(self.vars + ['formula'])

        for args in product(*repeat((False, True), len(self.vars))):
            print(args + (eval(self.translate(args, logic_formula)),))
            self.table.append(args)
            self.result_of_table.append(eval(self.translate(args, logic_formula)))

    def create_snf(self, vars_boolean, sknf):
        snf = ''
        or_or_and = 'v' if sknf else '^'
        for index in range(0, len(self.vars)):
            if not index == 0:
                snf = snf + ' ' + or_or_and + ' '
            if (vars_boolean[index] and not sknf) or (not vars_boolean[index] and sknf):
                snf = snf + self.vars[index]
            else:
                snf = snf + '-' + self.vars[index]
        return snf

    def create_nf(self, sknf):
        output = ''
        and_or_or = '^' if sknf else 'v'
        for index in range(0, len(self.result_of_table)):
            if (self.result_of_table[index] and not sknf) or (not self.result_of_table[index] and sknf):
                if not str(output) == '':
                    output = output + ' ' + and_or_or + ' '
                output = output + '(' + self.create_snf(self.table[index], sknf) + ')'
        return output


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


def calculation_method_str(formula, is_sknf_or_sdnf, counter):
    result = calculation_method(formula, is_sknf_or_sdnf)
    if is_sknf_or_sdnf:
        for i in range(0, counter - 2):
            result = calculation_method(result, is_sknf_or_sdnf)
    else:
        for i in range(0, counter - 2):
            result = calculation_method(result, is_sknf_or_sdnf)
    return result


def check(table):
    checker = ['X'] * len(table[0])
    for_check = [''] * len(table[0])
    for obj in table:
        for index, item in enumerate(obj):
            if item == 'X' and for_check[index] == '':
                for_check[index] = 'X'
    return checker == for_check

def kvain_mac_clascki(table):
    result = []
    for amount in range(1, len(table) - 1):
        buffer = combinations(table, amount)
        for obj in buffer:
            if check(obj):
                result.append(obj)
        if len(result) != 0:
            return result



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
