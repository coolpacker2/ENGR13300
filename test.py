import math
import statistics

a = 8
b = 3**(a/3)
c = math.cos(b**(1/2))
c = -0.37615246
d = math.floor(13*c)
e = 613%d
lol = [a, b, c, d, e]

average = statistics.mean(lol)
median = statistics.median(lol)
max_val = max(lol)
range_val = max(lol) - min(lol)
std_dev = statistics.stdev(lol)

print(average)