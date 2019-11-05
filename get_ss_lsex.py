# Scrape Stock Symbols for LSEX
# Manually get the URL for landmark filtered Stock Symbols from the London Stock Exhange, this code then
# amend the config file with number of pages and URL, and additionally filename.  

import urllib.request as req
import configparser
import re

config = configparser.ConfigParser()
config.read('config.cfg')

LANDMARK_LONDON_STOCK_SYMBOLS = config['LSEX']['url']
PAGES_TO_TRAVERSE = int(config['LSEX']['pages'])
FILE_TO_WRITE = config['OUTPUT']['filename']

symbols_written = 0
matcher = re.compile(r'<td scope="row" class="name">[A-Z0-9]*')

with open(FILE_TO_WRITE, 'a') as f:
    f.write('stock_symbol\n')
    print("File opened ...")
    for i in range(PAGES_TO_TRAVERSE):
        url = LANDMARK_LONDON_STOCK_SYMBOLS+str(i+1)
        print(url)
        url_open = req.urlopen(url)
        url_bytes = url_open.read()
        url_str = url_bytes.decode('utf8')
        url_open.close()
        print(f'url {url} read ...')
        
        results = matcher.findall(url_str)
        print(f'matched {len(results)} results')

        per_file_write = 0
        for match in results:
            f.write(match[match.find('>')+1:]+'\n')
            per_file_write += 1
        print(f'Written {per_file_write} symbols')    
        symbols_written += per_file_write

print(f'Symbols written {symbols_written} to {FILE_TO_WRITE}')






