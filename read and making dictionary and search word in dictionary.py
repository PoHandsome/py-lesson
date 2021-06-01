data = []
dic = {}

with open ('reviews.txt', 'r') as f:
    for l in f:
        data.append(str.lower(l))

for ing in data:
    words = ing.split()
    for j in words:
        if j in dic:
            dic[j] += 1
        else:
            dic[j] = 1
# for j in words:
#     if dic[j] > 10000:
#         print(j, dic[j])

while True:
    search_word = input('Please enter the word you want to search: ')
    if search_word == 'q':
        print('Thanks for using this searching function.')
        break
    elif search_word not in dic:
        print('Word not found in the dictionary.')
    else:
        print(search_word, ' has been found ',  dic[search_word], ' times.')