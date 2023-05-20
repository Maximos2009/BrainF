class Interpreter():
    def __init__(self):
        self.__array_size = 30_000
        self.__array = [0 for _ in range(self.__array_size)]
        self.__byte = 0
        self.__iterations = 0
        self.__error = False
        self.__opening_bracket_error = 'MISSING OPENING BRACKET'
        self.__closing_bracket_error = 'MISSING CLOSING BRACKET'
        self.__iteration_error = 'EXCEED ITERATION LIMIT'
        self.__iteration_limit = 1_000_000

    def get_array(self, start, end):
        return self.__array[start:end]

    def get_byte(self):
        return self.__byte

    def get_value(self):
        return self.__array[self.__byte]

    def get_error(self):
        return self.__error

    def set_array_size(self, new_size):
        if new_size > self.__array_size:
            self.__array += [0 for _ in range(new_size - self.__array_size)]
        elif new_size < self.__array_size:
            self.__array = self.__array[0: new_size]
        self.__array_size = new_size
        if self.__byte > new_size - 1:
            self.__byte = new_size - 1

    def set_iteration_limit(self, new_limit):
        if new_limit > 0:
            self.__iteration_limit = new_limit

    def execute(self, code):
        self.__iterations += 1

        if self.__iterations >= self.__iteration_limit:
            print(self.__iteration_error, end = '', flush = True)
            self.__error = True
            return

        for idx, char in enumerate(code):
            if char == '+':
                self.__array[self.__byte] += 1
                if self.__array[self.__byte] > 255:
                    self.__array[self.__byte] = 0
            elif char == '-':
                self.__array[self.__byte] -= 1
                if self.__array[self.__byte] < 0:
                    self.__array[self.__byte] = 255
            elif char == '>':
                self.__byte += 1
                if self.__byte > self.__array_size - 1:
                    self.__byte = 0
            elif char == '<':
                self.__byte -= 1
                if self.__byte < 0:
                    self.__byte = self.__array_size - 1
            elif char == '.':
                try:
                    print(chr(self.__array[self.__byte]), end = '', flush = True)
                except ValueError:
                    print('?', end = '', flush = True)
            elif char == ',':
                try:
                    user_input = input()
                    if user_input:
                        self.__array[self.__byte] = ord(user_input[0])
                except EOFError:
                    self.__array[self.__byte] = 0
            elif char == '[':
                start = idx + 1

                opens = 0
                closes = 0

                for subidx, subchar in enumerate(code[idx:]):
                    if subchar == '[':
                        opens += 1
                    elif subchar == ']':
                        closes += 1

                    if opens == closes:
                        end = idx + subidx
                        break
                else:
                    if not self.__error:
                        if opens > closes:
                            print(self.__closing_bracket_error, end = '', flush = True)
                        else:
                            print(self.__opening_bracket_error, end = '', flush = True)
                        self.__error = True
                    return

                subcode = code[start:end]

                while self.__array[self.__byte] != 0 and not self.__error and self.__iterations < self.__iteration_limit:
                    self.execute(subcode)

                if not self.__error:
                    self.execute(code[end + 1:])

                break
            elif char == ']':
                if not self.__error:
                    print(self.__opening_bracket_error, end = '', flush = True)
                    self.__error = True
                    return


def main():
    ip = Interpreter()
    filepath = input('Enter file path: ')

    while True:
        if filepath[0:3] not in ['C:/', 'C:\\']:
            filepath = input('Enter full file path (e.g. C:\\Users\\Joe\\Desktop\\MyProgram.b): ')
            continue

        try:
            with open(filepath, 'r') as file:
                program = file.read()
                break
        except FileNotFoundError:
            filepath = input('File not found. Try again: ')
        except PermissionError:
            filepath = input('Not a file. Try again: ')

    ip.execute(program)
    input(f'\n\nProgram finished with exit code {int(ip.get_error())}.\nPress ENTER to exit console.')


if __name__ == '__main__':
    main()
