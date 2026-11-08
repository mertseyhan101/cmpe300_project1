"""Independent reference interpreter for Algorithm 1.

Written separately from the submitted program: every `for` loop is expanded into
its while-loop form (init; test; body; increment) and execution counts are kept
per pseudocode line in a dictionary. The operation groups are derived from the
per-line counts afterwards, using the markers of the project PDF:

    (1) comparisons     : lines 3, 8
    (2) loop increments : lines 9, 15
    (3) assignments     : lines 4, 10, 14
    (4) assignments     : lines 7, 12, 16
"""

from collections import Counter

GROUP_LINES = {1: ("3", "8"), 2: ("9inc", "15inc"), 3: ("4", "10", "14"), 4: ("7", "12", "16")}


def run(text, d):
    arr = list(text)
    n = len(arr)
    line = Counter()
    res = 0
    s = 0
    i = 0
    while i <= n - 1:                       # line 2
        line["3"] += 1
        if arr[i] == "a":
            line["4"] += 1
            s = s + 1
            k = n                           # line 5
            while k > 0:                    # line 6
                line["7"] += 1
                k = k // d
        else:
            line["8"] += 1
            if arr[i] == "b":
                q = 0                       # line 9 init
                while q <= s:               # line 9 test
                    line["10"] += 1
                    res = res + q
                    r = 1                   # line 11 init
                    while r <= n:
                        line["12"] += 1
                        res = res + r
                        r = r + 1           # line 11 increment (unmarked)
                    line["9inc"] += 1
                    q = q + 1               # line 9 increment
            else:
                line["14"] += 1
                s = 0
                t = i                       # line 15 init
                while t <= n - 1:
                    line["16"] += 1
                    res = res + t
                    line["15inc"] += 1
                    t = t + 1               # line 15 increment
        i = i + 1
    groups = [sum(line[l] for l in GROUP_LINES[g]) for g in (1, 2, 3, 4)]
    return res, groups, line
