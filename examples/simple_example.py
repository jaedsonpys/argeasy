from random import randint
from argeasy import ArgEasy

COLORS = {
    'red': '\033[31m',
    'green': '\033[32m',
    'blue': '\033[34m',
    'close': '\033[m'
}


def main():
    argeasy = ArgEasy(
        description='Test of ArgEasy project',
        version='1.0.0',
        project_name='ArgEasy'
    )

    argeasy.add_argument('say', 'Say something')
    argeasy.add_argument('check_numbers', 'Analyzes whether the numbers are even', action='append')
    argeasy.add_argument('random', 'Generate random numbers', action='store_true')

    argeasy.add_flag('-c', 'Select color of text (RGB)')
    argeasy.add_flag('-m', 'Max range numbers')

    args = argeasy.get_args()

    if args.say:
        if args.c:
            if args.c == 'close':
                print('\033[31mChoose a valid color\033[m')
                return 0
            
            get_color = COLORS.get(args.c)
            close = COLORS.get('close')

            if not get_color:
                print('\033[31mChoose a valid color\033[m')
            else:
                print(get_color + args.say + close)
        else:
            print(args.say)
    elif args.check_numbers is not None:
        numbers = args.check_numbers
        even_numbers = []
        for n in numbers:
            if int(n) % 2 == 0:
                even_numbers.append(n)

        print(f'The even numbers are: {even_numbers}')
    elif args.random:
        if not args.m:
            print(randint(0, 9999))
        else:
            limit = int(args.m)
            print(randint(0, limit))


main()
