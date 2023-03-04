from functions import parser_string, wrong_command, help_
from decorator import input_error
from classes import synk, save


@input_error
def notebook_main():
    try:
        while True:
            u_input = input('Enter command ')  # ---------   Добавить образцы команд   -------------
            handler, *args = parser_string(u_input)
            if handler == wrong_command:
                print('Wrong command(')
            elif handler == exit:
                print("Good bye!")
                break
            else:
                result = handler(*args)
                print(result)
    finally:
        save()


def run():
    synk()
    print('Welcome to NoteBook')
    print(help_())
    notebook_main()


if __name__ == '__main__':
    run()
