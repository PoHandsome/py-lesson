products = []
while True:
    name = input('Please enter product name: ')
    if name == 'q':
        break
    price = input('Please enter product price: ')    
    products.append([name,price])
print(products)

for p in products:
    print('Price of ', p[0], ' is ', p[1])