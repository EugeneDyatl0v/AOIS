from itertools import product, repeat
from multipledispatch import dispatch

class AOIS4:
    sumator_table = []
    result_table = []
    table_of_x = []
    table_of_y = []
    result_tables = []
    vars = ['A', 'B', 'C']
    imaginary_unit = 0

    # summing_bytes sum_in_direct_code --- методы для сложения двоичных чисел
    def summing_bytes(self, byte_1, byte_2):
        amount_of_bytes = int(byte_1) + int(byte_2) + self.imaginary_unit
        if amount_of_bytes < 2:
            output = amount_of_bytes
            self.imaginary_unit = 0
        else:
            output = amount_of_bytes - 2
            self.imaginary_unit = 1
        return output

    def sum_in_direct_code(self, number_in_binary_code_1):
        number_in_binary_code_2 = (0, 1, 1, 0)

        for i in range(3, -1, -1):
            number_in_binary_code_1[i] = self.summing_bytes(number_in_binary_code_1[i], number_in_binary_code_2[i])
        self.imaginary_unit = 0
        return number_in_binary_code_1
    
    # transform calculation_method calculation_method_str --- методы для минимизации
    def transform(self, formula, is_sknf_or_sdnf):
        first_operator = 'v' if is_sknf_or_sdnf else '^'
        second_operator = '^' if is_sknf_or_sdnf else 'v'
        formula = formula.replace(first_operator, '').replace(' (', '').replace(') ', '').replace('(', '').replace(')',
                                                                                                                   '')
        sts = formula.split(second_operator)
        buffer = []
        for st in sts:
            st = st.split('  ')
            buffer.append(st)
        sts = buffer
        return sts

    def calculation_method(self, formula, is_sknf_or_sdnf):
        first_operator = 'v' if is_sknf_or_sdnf else '^'
        second_operator = '^' if is_sknf_or_sdnf else 'v'

        sts = self.transform(formula, is_sknf_or_sdnf)

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

    def calculation_method_str(self, formula, is_sknf_or_sdnf, counter):
        result = self.calculation_method(formula, is_sknf_or_sdnf)
        if is_sknf_or_sdnf:
            for i in range(0, counter - 2):
                result = self.calculation_method(result, is_sknf_or_sdnf)
        else:
            for i in range(0, counter - 2):
                result = self.calculation_method(result, is_sknf_or_sdnf)
        return result
    # create_snf и create_nf построение сднф или скнф
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

    @dispatch(bool, int)
    def create_nf(self, sknf, s_or_p):
        output = ''
        and_or_or = '^' if sknf else 'v'
        for index in range(0, len(self.result_table)):
            if (self.result_table[index][s_or_p] and not sknf) or (not self.result_table[index][s_or_p] and sknf):
                if not str(output) == '':
                    output = output + ' ' + and_or_or + ' '
                output = output + '(' + self.create_snf(self.sumator_table[index], sknf) + ')'
        return output

    @dispatch(bool, list)
    def create_nf(self, sknf, result_table):
        output = ''
        and_or_or = '^' if sknf else 'v'
        for index in range(0, len(result_table)):
            if (result_table[index] and not sknf) or (not result_table[index] and sknf):
                if not str(output) == '':
                    output = output + ' ' + and_or_or + ' '
                output = output + '(' + self.create_snf(self.table_of_x[index], sknf) + ')'
        return output

    # Получение переменных P и S
    def find_p_and_s(self, args):
        if args.count(True) == 3:
            p = 1
            s = 1
        elif args.count(True) == 2:
            p = 1
            s = 0
        elif args.count(True) == 1:
            p = 0
            s = 1
        else:
            p = 0
            s = 0
        return p, s

    # Построение таблицы для первого задания
    def create_table(self):
        print(self.vars + ['P', 'S'])

        for args in product(*repeat((False, True), len(self.vars))):
            print(args + (self.find_p_and_s(args)))
            self.sumator_table.append(args)
            self.result_table.append(self.find_p_and_s(args))

    # Создание таблицы для второго задания
    def create_table_of_x_and_y(self):
        for args in product(*repeat((0, 1), 4)):
            self.table_of_x.append(list(args))
            self.table_of_y.append(list(args))
        for i in range(0, 10):
            self.sum_in_direct_code(self.table_of_y[i])
        self.table_of_y = self.table_of_y[:-6]

    # Вывод таблицы для 2 задания
    def print_tables(self):
        for i in range(4, 0, -1):
            print('x' + str(i), end='   ')
            for j in range(0, len(self.table_of_x)):
                print(self.table_of_x[j][3 - (i - 1)], end=' ')
            print('\n')
        print('-' * 36)
        for i in range(4, 0, -1):
            print('y' + str(i), end='   ')
            for j in range(0, len(self.table_of_y)):
                print(self.table_of_y[j][3 - (i - 1)], end=' ')
            print('\n')

    def get_result_tables(self):
        for i in range(0, 4):
            buffer = []
            for j in range(0, len(self.table_of_y)):
                buffer.append(self.table_of_y[j][i])
            self.result_tables.append(buffer)


if __name__ == '__main__':
    example = AOIS4()
    example.create_table()
    print('----------------------------СДНФ-P--------------------------')
    print(example.create_nf(False, 0))
    print('----------------------------СДНФ-S--------------------------')
    print(example.create_nf(False, 1))
    print('---------------------Минимизация-S--------------------------')
    print(example.calculation_method_str(example.create_nf(False, 0), False, 3))
    print('---------------------Минимизация-P--------------------------')
    print(example.calculation_method_str(example.create_nf(False, 1), False, 3))
    print('\n\n')
    example.create_table_of_x_and_y()
    example.get_result_tables()
    example.print_tables()
    example.vars = ['D', 'C', 'B', 'A']
    for i in range(3, -1, -1):
        print('------------------------------------------------------------------------------------СДНФ-' + str(4-i) +
              '------------------------------------------------------')
        print(
            example.create_nf(False, example.result_tables[i]).replace('D', 'x4').replace('C', 'x3').replace(
                'B', 'x2').replace('A', 'x1'))
    for i in range(3, -1, -1):
        print('-----------------------------------------------------------------------------Минимизация-' + str(4 - i) +
              '------------------------------------------------------')
        print(example.calculation_method_str(example.create_nf(False, example.result_tables[i]), False, 4).replace(
            'D', 'x4').replace('C', 'x3').replace('B', 'x2').replace('A', 'x1'))