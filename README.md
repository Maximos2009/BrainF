# Brainfuck Interpreter
An interpreter for the brainfuck programming language.

## Brainfuck Tutorial
You have:
* An `array` filled with thirty thousand zeros
* A `pointer` that points to which element of the array you want to edit

Brainfuck has these 8 commands that you can use:
* `+`: Increases the element of the `array` that the `pointer` is pointing to by one
* `-`: Decreases the element of the `array` that the `pointer` is pointing to by one
* `>`: Makes the `pointer` point to the next element of the `array`
* `<`: Makes the `pointer` point to the previous element of the `array`
* `.`: Prints the character with the [ASCII value](https://www.asciitable.com/) of the element of the `array` that the `pointer` is pointing to
* `,`: Asks for input and then sets the element of the `array` that the `pointer` is pointing to to the [ASCII value](https://www.asciitable.com/) of the input
* `[`: Defines the start of a loop that continues until the element that the `pointer` is pointing to is zero
* `]`: Defines the end of a loop that continues until the element that the `pointer` is pointing to is zero

## How it works
There is an `Interpreter` class.
Each object of that class has these protected properties:
* `array_size`: The size of the array. Can be changed with the `set_array_size()` method
* `array`: The array with a length of `array_size`
* `byte`: The pointer
* `iterations`: Number of times the `execute()` method has ran. Useful for detecting infinite loops
* `error`: Stores whether an error has occured
* `opening_bracket_error`: The message printed when an opening bracket is missing
* `closing_bracket_error`: The message printed when a closing bracket is missing
* `iteration_error`: The message printed when `iterations` exceeds `iteration_limit`
* `iteration_limit`: The number of times the `execute()` method can be ran before an exception is raised

And these methods:
* `get_array(start, end)`: Returns the `array` from the index `start` until the index `end`
* `get_byte()`: Returns the `byte` property
* `get_value()`: Returns the `array`'s element with the index of `byte`
* `get_error()`: Return the `error` property
* `set_array_size(new_size)`: Sets the object's `array_size` property to `new_size`. If the `byte` property is over `new_size` then it is set to `new_size - 1`
* `set_iteration_limit(new_limit)`: Sets the object's `iteration_limit` property to `new_limit`. Does nothing if `new_limit` is less than one
* `execute(code)`: This method will be discussed in the next chapter

## The `execute()` method
Increases the `iterations` property by one.
Checks if the `iterations` property is over the `iteration_limit` property. If yes, the `iteration_limit_error` property is printed, the `error` property becomes `True` and the execution ends.
Iterates through every character of `code` with the character called `char` and its index called `idx`:
* If `char` is `+`, increases the element of `array` with index of `byte` by one. If the value that was increased is now larger than two hundred and fifty five, it becomes zero
* If `char` is `-`,  decreases the element of `array` with index of `byte` by one. If the value that was decreased is now smaller than zero, it becomes two hundred and fifty five
* If `char` is `>`, increases `byte` by one. If `byte` is now larger than the `array_size - 1` property, it is set to zero
* If `char` is `<`, decreases `byte` by one. If `byte` is now smaller than zero, it is set to the `array_size - 1`
* If `char` is `.`, prints the character with the [ASCII value](https://www.asciitable.com/) of the element of the `array` with index of `byte` using the chr function. If a `ValueError` is raised because the argument in `chr` is not in `range(0x110000)`, the element of the `array` is set to zero
* If `char` is `,`, asks for input and then sets the element of the `array` with the index of `byte` to the [ASCII value](https://www.asciitable.com/) of the input. If an `EOFError` is raised the element is set to zero
* If `char` is `[`, a variable called `start` is initialized with the value of `idx + 1`. Two variables called `opens` and `closes` are initialized both of which with the value of zero. Iterates through every character of `code` from `idx` until the end with the character called `subchar` and its index called `subidx`. If subchar is `[`, `opens` is inreased by one. If subchar is `]`, `closes` is increased by one. If `opens` is equal to `closes`, a variable called `end` is initialized with the value of `idx + subidx` and the loop ends. If the loop ends without `opens` ever being equal to `closes` and the `error` property is set to `False`, if `opens` is larger than `closes` the `closing_bracket_error` property is printed. Else the `opening_bracket_error` property is printed. Then the `error` property is set to `True` and the execution stops. Now going back to the loop, if it ended successfully, a variable called `subcode` is initialized with the value of `code` from `start` until `end`. While the element of `array` with the index of `byte` is not equal to zero and the `error` property is set to `False` and the `iterations` property is less than the `iteration_limit` property, recursion is used and the `execute()` method is called with the `code` argument being `subcode`. After the loop ends, if the `error` property is set to `False`, the `execute()` method is called with the `code` argument being `code` from `end + 1` untill the end. And finally the loop ends.
* If `char` is `]` and the `error` property is set to `False`, the `opening_bracket_error` property is printed, the `error` property is set to `True` and the execution stops. All that happends because when there is a loop ends, the code is executed from the end of the loop untill the end meaning the interpreter would normally never see a closing bracket.
* Every other character is interpreted as a comment

## The `main()` method
An `Interpreter` object is initialized with the name of `ip`.
The user is asked for the path of a brainfuck file and a variable called `filepath` is initialized with the value of the input.
An infinite loop starts.
If the first three letters of `filepath` are not `C:/` or `C:\`, the user is reminded that they have to submit the full file path and not just the file name and is asked again for the file path. After that a continue statement is used.
Else the program tries to open `filepath`. If it succeeds, it breaks out of the loop. If a `FileNotFoundError` is raised, the user is informed and is asked for another path. If a `PermissionError` is raised, the user is informed that they submited a path to a directory instead of a file and again is asked for another path.
If the file is found, it is used as the `code` argument in the `ip`'s `execute()` method.
After the file has been executed the exit code, which is `ip`'s `get_error()` method , is printed and the program ends.

## The `test.b` file
This file's content is this:
```
>+++++++++[<++++++++>-]<.            H
>>++++++++++[<++++++++++>-]<+.       e
+++++++.                             l
.                                    l
+++.                                 o
>>++++++++[<++++>-]<.              SPACE
<<+++++++++++++++.                   W
>.                                   o
+++.                                 r
------.                              l
--------.                            d
>+.                                  !
```
But let's discuss how it works.
First of all a trick used in brainfuck programming is multiplication. You set an element of the `array` to have a value of `x`. While `x` is larger than 0 you go to an other element and you increase it by `y`. Then you go back to the other byte and decrease it by one and repeat. If for example `x = 3` and `y = 2`, then at the end the value of the second byte will be six. Notice how 6 = 3 * 2. So this trick multiplies `x` by `y`.

Also you should have the [ASCII table](https://www.asciitable.com/) open in another tab.

The first line sets the value of the first byte to `9 * 8 = 72` and then prints `H`
The second line sets the second byte to `11 * 10 = 110` and increases it by one so that's `e`
Then, in the third line the second byte is increased by 7 and an `l` is printed
After that, the same letter is printed
Following that, the second byte is increased by 3 and an `o` appears on the screen
On the sixth line the third byte is set to `8 * 4 = 32` which is a `(space)`
On the next line we go back to the first byte, increase it by 15 and print `W`
After that line we go back to the second byte and print an `o`
Coming on the next line, we increase the second byte by 3 and `r` is printed
Then we decrease the second byte by 6 and that gives us an `l`
Approaching the end, we decrease the second byte by 8 and we get a `d`
And finally, we go to the third byte, increase it by one and print `!`
