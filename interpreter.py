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
        self.iteration_limit = 1_000_000
        self.input_allowed = True

    def change_array_size(self, new_size):
        if new_size > self.__array_size:
            self.__array += [0 for _ in range(new_size - self.__array_size)]
        elif new_size < self.__array_size:
            self.__array = self.__array[0: new_size]
        self.__array_size = new_size

    def get_array(self, start, end):
        return self.__array[start:end]

    def get_byte(self):
        return self.__byte

    def get_value(self):
        return self.__array[self.__byte]
    
    def get_error(self):
        return self.__error

    def execute(self, code):
        self.__iterations += 1

        if self.__iterations == 99_999:
            pass

        if self.__iterations >= self.iteration_limit:
            print(self.__iteration_error, end='', flush=True)
            self.__error = True
            code = ''

        for idx, char in enumerate(code):
            if char == '+':
                if self.__array[self.__byte] >= 255:
                    self.__array[self.__byte] = 0
                else:
                    self.__array[self.__byte] += 1
            elif char == '-':
                if self.__array[self.__byte] <= 0:
                    self.__array[self.__byte] = 255
                else:
                    self.__array[self.__byte] -= 1
            elif char == '>':
                if self.__byte < self.__array_size - 1:
                    self.__byte += 1
                else:
                    self.__byte = 0
            elif char == '<':
                if self.__byte > 0:
                    self.__byte -= 1
                else:
                    self.__byte = self.__array_size - 1
            elif char == '.':
                try:
                    print(chr(self.__array[self.__byte]), end='', flush=True)
                except ValueError:
                    print('?', end='', flush=True)
            elif char == ',':
                # TODO: Fix
                if self.input_allowed:
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
                        end = subidx + start - 1
                        break
                else:
                    if not self.__error:
                        if opens < closes:
                            print(self.__opening_bracket_error, end='', flush=True)
                        else:
                            print(self.__closing_bracket_error, end='', flush=True)
                        self.__error = True
                    break

                subcode = code[start:end]

                while self.__array[self.__byte] != 0 and not self.__error and self.__iterations < self.iteration_limit:
                    self.execute(subcode)

                if not self.__error:
                    self.execute(code[end + 1:])

                break
            elif char == ']':
                if not self.__error:
                    print(self.__opening_bracket_error, end='', flush=True)
                    self.__error = True
                    break


def main():
    ip = Interpreter()
    filename = input('Enter file path: ')

    while True:
        if filename[0:3] not in ['C:/', 'C:\\']:
            filename = input('Enter full file path (e.g. C:\\Users\\Joe\\Desktop\\MyProgram.b): ')
            continue

        try:
            with open(filename, 'r') as file:
                program = file.read()
                break

        except FileNotFoundError:
            filename = input('File not found. Try again: ')
        except PermissionError:
            filename = input('Not a file. Try again: ')
    
    ip.execute(program)
    input(f'\n\nProgram finished with exit code {int(ip.get_error())}.\nPress ENTER to exit console.')


if __name__ == '__main__':
    main()
