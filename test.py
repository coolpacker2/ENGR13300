x = 3
y = 6
i = 1
while i < 10:
    print(f"Starting while loop iteration: i = {i}, x = {x}, y = {y}")
    for z in [x, y]:
        i += z
        print(f"  Added {z} to i. New i = {i}")
    if x < 3:
        x += 1
        print(f"  Incremented x; Current x = {x}")
print(f"Final value of i: {i}")