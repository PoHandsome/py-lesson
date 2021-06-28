from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from datetime import datetime, timedelta
import re
import json
import os
import time
import sys

import requests
from bs4 import BeautifulSoup as bs

def multi_title(head, num):
    res = []
    n = int(12/num) 
    for i in range(n):
        res.extend([head[i]] * num)
    return res

def crawl(date):
    query_date = f'{date.year}%2F{date.month}%2F{date.day}'
    r = requests.get(f'https://www.taifex.com.tw/cht/3/futContractsDate?quertType=1&doQuery=1&queryDate={query_date}')
    data = {}
    try:
        if r.status_code == requests.codes.ok:
            soup = bs(r.text, 'html.parser')
            table = soup.find('table', attrs = {'class':'table_f'})
            lines = table.find_all('tr') 
    except:
        return data, date
    
    rows = lines[3:-4]
    head1 = lines[0].text.strip().split()
    head_1 = multi_title(head1, 6)
    head2 = lines[1].text.strip().split()
    head_2 = multi_title(head2, 2)
    head3 = lines[2].text.strip().split()[2:]
    header = []
    for i in range(len(head_1)):
        header.append(head_1[i]+head_2[i]+head3[i])
    headers = lines[2].text.strip().split()[:2] + header
    for line in rows:
        ths = line.find_all('th')
        titles = [i.text.strip() for i in ths]
        
        if len(titles) == 3:
            product = titles[1]
            who = titles[2]
        else:
            who = titles[0]

        tds = line.find_all('td')
        cells = [i.text.strip() for i in tds]
        
        row_data = [product, who] + cells
        
        convert_int = [int(d.replace(',', '')) for d in row_data[2:]]
        row_data = row_data[:2] + convert_int

        product = row_data[0]
        who = row_data[1]
        contents = {headers[i]: row_data[i] for i in range(2, len(headers))}

        if product not in data:
            data[product] = {who:contents}
        else:
            data[product][who] = contents
    return data, date
    
def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii = False, indent = 4) #ensure all word can be saved correctly
    print('save flie to ', filename)

def main():
    today = datetime.today()
    date = today
    download_dir = 'futures'
    os.makedirs(download_dir, exist_ok = True)
    get_days = 10
    datas = []
    start_time = time.time()
    date_list = []
    count = 0
    with ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            filename = f'future_{date.strftime("%Y%m%d")}.json'
            filename = os.path.join(download_dir, filename)
            if os.path.isfile(filename):
                print('file exists')
                date_list.append(date)
                date = date - timedelta(days=1)
                count += 1
                continue
            data = executor.submit(crawl, date)
            datas.append(data)
            date = date - timedelta(days=1)
            if date < today - timedelta(days=1085):
                break
       
        if count >= 720:
            done, not_done = wait(datas, timeout = 0)
            for nd in not_done:
                nd.cancel()
        else:
            for d in as_completed(datas):
                if not d.result()[0]:
                    print('data exist already!')
                    continue
                if d.result():
                    data, date = d.result()
                    filename = f'future_{date.strftime("%Y%m%d")}.json'
                    filename = os.path.join(download_dir, filename)
                    save_json(data, filename)
                else:
                    print(f'no data in {date}')
                    continue
                print('still in for loop')
    end_time = time.time()
    total_time = end_time - start_time
    print(f'spend {"%.2f" % total_time} seconds')
if __name__ == '__main__':
    main()

