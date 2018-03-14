from builtins import input


def ask_for_input(prompt, allowed, input_fn=input, exit_fn=exit):
    i = input_fn(prompt)
    while i not in allowed and i != 'exit':
        i = input_fn(prompt)
    if i == 'exit':
        exit_fn()
    return i
