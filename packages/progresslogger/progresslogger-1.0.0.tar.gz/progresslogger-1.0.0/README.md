# Progress Logger
## `pip install progresslogger`

Progress Logger is a simple, lightweight logger for your Python loops. Quickly see the current status of long loops, its estimated time remaining, and more useful stats!

---

### Simple Usage

Progress Logger works great right out of the box, with no customization required. When imported, it will overwrite the built-in `enumerate()` function. That's it!

```
from progresslogger import *

my_list = ['a', 'b', 'c', 'd', 'e']

for i, letter in enumerate(my_list):
    execute_code(letter)
```

<br>

Output:
```
>>> Starting progress logger for 5 items.
>>> Iteration 1 of 5 (20.0%) complete. Approximately 4 seconds remaining.
>>> Iteration 2 of 5 (40.0%) complete. Approximately 3 seconds remaining.
>>> ...
>>> Loop complete! Average iteration time: 1.0 seconds
```

---

### Advanced Usage

You may customize your logger and pass it directly to the `enumerate()` function:
```
my_logger = ProgressLogger(show_next_value=True)
for i, letter in enumerate(my_list, my_logger):
    execute_code(letter)
```

<br>

Output:
```
>>> Starting progress logger for 5 items. Next value: "a".
>>> Iteration 1 of 5 (20.0%) complete. Approximately 4 seconds remaining. Next value: "b".
>>> Iteration 2 of 5 (40.0%) complete. Approximately 3 seconds remaining. Next value: "c".
>>> ...
```

<br>

If you'd like to retain the built-in `enumerate()` function, or you'd like to have both, you can use `from progresslogger import ProgressLogger` or `import progresslogger` and use `progresslogger.enumerate(...)`.

You may wish to insert the log in the middle of a loop, or otherwise implement your logger yourself. Simply initialize `ProgressLogger` before the loop, and call `mylogger.log()` once each loop:
```
my_logger = ProgressLogger(my_list) # be sure to pass your collection when initializing your logger
for letter in my_list:
    my_logger.log()
    execute_code(letter)
```