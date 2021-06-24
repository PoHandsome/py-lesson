import sys
import getopt
from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def print_usage():
    print('python big_8_stock.py -o <output file type>')
    print('available file types: csv , json , html')

#Comment Line Arguments
def cla():
    short_opts = 'ho:'
    long_opts = 'help output='.split()
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
        return opts
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

def main():
    opts = cla()
    output_type = 'csv'
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_usage()
            sys.exit(0)
        elif opt in ('-o', '--output'):
            output_type = arg
    if output_type not in ('csv', 'json', 'html'):
        print(f'no {arg} file type or {arg} is not supported in this version')
        sys.exit(0)

    data = []
    r = requests.get('https://chart.capital.com.tw/Chart/TWII/TAIEX11.aspx')
    soup = bs(r.text, 'html.parser')
    tables = soup.find_all('table', attrs = {'cellpadding':'5'})  
    for line in tables:    
        lines = line.find_all('tr')
        for i in lines:
            date, value, price = [j for j in i.text.split()[:3]]
            if not price.isnumeric():
                continue
            data.append([date, value, price])

    df = pd.DataFrame(data, columns =['date', 'value', 'price'])
    now = datetime.now().strftime('%Y-%m-%d')

    if output_type == 'csv':
        df.to_csv(f'{now}_big_eight.csv')
    elif output_type == 'json':
        df.to_json(f'{now}_big_eight.json')
    elif output_type == 'html':
        df.to_html(f'{now}_big_eight.html')

if __name__ == '__main__':
    main()
