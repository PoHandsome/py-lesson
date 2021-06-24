import requests
from bs4 import BeautifulSoup as bs

def main():
    while True:
        input_num = input('Please enter the stock number you want to search:')
        if input_num in ['q', 'quit', '']:
            break
        elif input_num.isnumeric():
            stock_num = input_num
        else:
            print('Wrong type of input, please enter exist number!')
            continue
        try:
            r = requests.get(f'https://tw.stock.yahoo.com/q/q?s={stock_num}')
            if r.status_code == requests.codes.ok:
                soup = bs(r.text, 'html.parser')
                table = soup.find_all('table')[2]
                title = table.find_all(attrs={'width':55})
                value = table.find_all(attrs={'bgcolor':'#FFFfff'})
                stock_result = {title[i].text: value[i].text.split()[0] for i in range(len(title))}
                print(stock_result)
        except:
            print(f'no data found for stock number {input_num}')

if __name__ == '__main__':
    main()
