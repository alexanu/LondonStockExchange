# Scrape Stock Symbols for LSEX
# Manually get the URL for landmark filtered Stock Symbols from the London Stock Exhange, this code then
# amend the config file with number of pages and URL, and additionally filename.  

import urllib.request as req
import configparser
import re
import json


with open("config.json", "r") as f:
    config = json.load(f)

with open("all_industry_ustock_codes_from_funds.json", "r") as f:
    industry_codes = json.load(f)

INDUSTRY_CODES = config['USTOCK']['code']
URL = config['USTOCK']['url']
PAGES_TO_TRAVERSE = config['USTOCK']['pages']
FILE_TO_WRITE = config['OUTPUT']

symbols_written = 0
matcher = re.compile(r'{}'.format(config['USTOCK']['pattern']))

page = 0
for industry in industry_codes:
    ic = industry_codes[industry].replace("/", "_")
    with open(FILE_TO_WRITE.format(ic), 'a') as f:

        print(f'Opened file {industry_codes[industry]}')
        f.write('stock_symbol, company_name\n')
    
        while True:
            url = URL.format(code=industry, page=page)
            url_open = req.urlopen(url)
            url_bytes = url_open.read()
            url_str = url_bytes.decode('utf8')
            url_open.close()

            print(f'url {url} read ...')
        
            results = matcher.findall(url_str)
            if not results:
                break
            print(f'matched {len(results)} results')

            per_file_write = 0
            for match in results:
                code_st = match.find(">")+1
                code_ed = match.find("</td>")
                symbol_code = match[code_st:code_ed]
                desc_st = match.find("<div>")+5
                desc_ed = match.find("</div>")
                desc = match[desc_st:desc_ed]
                f.write("{},{}\n".format(symbol_code, desc))
                per_file_write += 1

            print(f'Written {per_file_write} symbols')    
            symbols_written += per_file_write
            page += 50
        page = 0
        per_file_write = 0

print(f'Symbols written {symbols_written} to {FILE_TO_WRITE}')
