data = []
y = 0

with open ('reviews.txt', 'r') as f:
    for l in f:
        data.append(l)
        y = y + len(l)

avg = y / len(data)

print('留言平均長度為', avg)

