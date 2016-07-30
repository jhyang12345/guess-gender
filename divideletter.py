import sys
from jamo import h2j, j2hcj
from collections import Counter

string = sys.stdin.readline().strip()

divided = []
for x in j2hcj(h2j(string)):
    divided.append(x)

counts = Counter()
for letter in divided:
    counts[letter] += 1

print(counts)
