import table


def load_table():
    table.add_value('Gramar', 'G=(N,D,G,S)')
    table.add_value('Theory', 'T=(A,D,G,L)')
    table.add_value('First Axiom', '((!A)~A)')
    table.add_value('Second Axiom', '((A/\B)~B)')
    table.add_value('Third Axiom', '(A~(A\/B))')
    table.add_value('Fourth Axiom', '(A->(B~A))')
    table.add_value('Boolean bundles', 'or-or-and')
    table.add_value('Subject domain', 'model of concepts')
    table.add_value('Problem domain', 'the part of reality')
    table.add_value('Prolog Language', 'programming on logic')
    table.add_value('First Formula', '(C~B)')
    table.add_value('Second Formula', '(D~A)')


def print_menu():
    print('0 -ADD')
    print('1 -Search')
    print('2 -Delete')
    print('3 -Print')
    print('4 -Exit')


def menu():
    print_menu()
    print('Input your CHOICE:\t')
    choice = input()
    while (choice != '4'):
        if choice == '0':
            key: str
            value: str
            key, value = input(), input()
            table.add_value(key, value)
        elif choice == '1':
            key: str
            value: str
            key = input()
            print(table.search(key))
        elif choice == '2':
            key: str
            value: str
            key = input()
            table.delete(key)
        elif choice == '3':
            table.print()

        print_menu()
        print('Input your choice:\t')
        choice = input()


table = table.hash()
load_table()
table.print()
menu()


