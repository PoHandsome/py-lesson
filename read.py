data = []
y = 0
count = 0

with open ('reviews.txt', 'r') as f:
    for l in f:
        data.append(l)
        y = y + len(l)

avg = y / len(data)

print('留言平均長度為', avg)


for d in data:
    if len(d) >= 100:
        count += 1
    else:
        pass

print('總共有', count, '筆資料長度為100以上')

good = []
for d in data:
    if 'good' in d:
        good.append(d)
print('總共有', len(good), '筆資料提到good')