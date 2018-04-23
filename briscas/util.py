from builtins import input

from briscas.models.core import Suite, Colors


def ask_for_input(prompt, allowed, input_fn=input, exit_fn=exit):
    i = input_fn(prompt)
    while i not in allowed and i != 'exit':
        i = input_fn(prompt)
    if i == 'exit':
        exit_fn()
    return i


def is_better(a, b, life):
    if a.suite == life.suite and b.suite != life.suite:
        return True
    elif a.suite != life.suite and b.suite == life.suite:
        return False
    elif a.suite == b.suite:
        return (
            a.number == 1 or
            (a.number == 3 and b.number != 1) or
            (b.number not in [1, 3] and a.number > b.number)
        )
    else:  # different non-life suites. first card wins.
        return True


def b(i, j):
    """Block coordinates"""
    return [(i, j), (i, j+1), (i+1, j), (i+1, j+1)]


CARD_LENGTH = L = 14
CARD_HEIGHT = H = 10
SYMBOL_LENGTH = SL = 2
SYMBOL = {
    Suite.ORO: Colors.YELLOW + '#' + Colors.RESET,
    Suite.BASTON: Colors.GREEN + '#' + Colors.RESET,
    Suite.ESPADA: Colors.BLUE + '#' + Colors.RESET,
    Suite.COPA: Colors.RED + '#' + Colors.RESET,
}
TOP_BOTTOM_BORDER = [' '] + ['-'] * (L - 2) + [' ']
EMPTY_LINE = ['|'] + [' '] * (L - 2) + ['|']
L2 = int(L / 2) - 1  # HALF LENGTH
H2 = int(H / 2) - 1  # HALF HEIGHT
L4 = int(L2 / 2)
H4 = int(H2 / 2)
SYMBOL_LOCATIONS = {
    1: [b(L2, H2)],
    2: [b(L2, H4), b(L2, H2 + H4)],
    3: [b(L2, H4 - 1), b(L2, H2), b(L2, H2 + H4 + 1)],
    4: [b(L4, H4), b(L4, H2 + H4),
        b(L2 + L4, H4), b(L2 + L4, H2 + H4)],
    5: [b(L4, H4), b(L4, H2 + H4),
        b(L2 + L4, H4), b(L2 + L4, H2 + H4),
        b(L2, H2)],
    6: [b(L4, H4 - 1), b(L4, H2), b(L4, H2 + H4 + 1),
        b(L2 + L4, H4 - 1), b(L2 + L4, H2), b(L2 + L4, H2 + H4 + 1)],
    7: [b(L4, H4 - 1), b(L4, H2), b(L4, H2 + H4 + 1),
        b(L2 + L4, H4 - 1), b(L2 + L4, H2), b(L2 + L4, H2 + H4 + 1),
        b(L2, H4)],
    8: [b(L4, H4 - 1), b(L4, H2), b(L4, H2 + H4 + 1),
        b(L2 + L4, H4 - 1), b(L2 + L4, H2), b(L2 + L4, H2 + H4 + 1),
        b(L2, H4), b(L2, H2 + H4)],
    9: [b(L4, H4 - 1), b(L4, H2), b(L4, H2 + H4 + 1),
        b(L2 + L4, H4 - 1), b(L2 + L4, H2), b(L2 + L4, H2 + H4 + 1),
        b(L2, H4 - 1), b(L2, H2), b(L2, H2 + H4 + 1)],
    10: [(L2 - 2, H2 - 2), (L2 - 2, H2 - 1),
         (L2 - 2, H2), (L2 - 2, H2 + 1), (L2 - 2, H2 + 2),
         (L2 + 1, H2 - 2), (L2 + 1, H2 - 1), (L2 + 1, H2),
         (L2 + 1, H2 + 1), (L2 + 1, H2 + 2),
         (L2 + 2, H2 - 2), (L2 + 2, H2 + 2),
         (L2 + 3, H2 - 2), (L2 + 3, H2 - 1), (L2 + 3, H2),
         (L2 + 3, H2 + 1), (L2 + 3, H2 + 2)],
    11: [(L2 - 2, H2 - 2), (L2 - 2, H2 - 1), (L2 - 2, H2),
         (L2 - 2, H2 + 1), (L2 - 2, H2 + 2),
         (L2 + 3, H2 - 2), (L2 + 3, H2 - 1), (L2 + 3, H2),
         (L2 + 3, H2 + 1), (L2 + 3, H2 + 2)],
    12: [(L2 - 2, H2 - 2), (L2 - 2, H2 - 1), (L2 - 2, H2),
         (L2 - 2, H2 + 1), (L2 - 2, H2 + 2),
         (L2 + 1, H2 - 2), (L2 + 1, H2), (L2 + 1, H2 + 1),
         (L2 + 1, H2 + 2),
         (L2 + 2, H2 - 2), (L2 + 2, H2), (L2 + 2, H2 + 2),
         (L2 + 3, H2 - 2), (L2 + 3, H2 - 1), (L2 + 3, H2), (L2 + 3, H2 + 2)],
}
# Flatten blocks.
for i in range(1, 10):
    SYMBOL_LOCATIONS[i] = [t for block in SYMBOL_LOCATIONS[i] for t in block]


def hand_string(hand):
    # Create empty matrix
    matrix = []
    matrix.append(TOP_BOTTOM_BORDER * len(hand))
    for i in range(H - 2):
        matrix.append(EMPTY_LINE * len(hand))
    matrix.append(TOP_BOTTOM_BORDER * len(hand))

    # Insert symbols
    o = 0  # offset
    for card in hand:
        s = SYMBOL[card.suite]
        matrix[1][o + L - 2] = str(card.number)[-1]
        matrix[H - 2][o + 1] = str(card.number)[0]
        if len(str(card.number)) > 1:  # Then add other digit
            matrix[1][o + L - 3] = str(card.number)[0]
            matrix[H - 2][o + 2] = str(card.number)[1]
        for (i, j) in SYMBOL_LOCATIONS[card.number]:
            matrix[j][o + i] = s
        o += CARD_LENGTH

    # Build into string
    string = '\n'.join([''.join(line) for line in matrix])
    return string
