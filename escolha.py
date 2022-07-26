from tabulate import tabulate
from .menu import menu_acc
from . import portugues, english, espanol


def main(password):
    print(tabulate(menu_acc, tablefmt="psql"))
    try:
        n = int(input("Input -> "))

        if n == 1:
            portugues.threadit(password)

        elif n == 2:
            english.threadit(password)

        elif n == 3:
            espanol.threadit(password)

        else:
            print("\n3RR0R")

    except Exception as g:
        print(g)



