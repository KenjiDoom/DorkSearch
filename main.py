import re, json, httpx, argparse, random, requests, urllib.parse
from bs4 import BeautifulSoup
from time import sleep

# User option here, but using command line
parser = argparse.ArgumentParser(description='Use a custom dork list and search a website')
parser.add_argument('--url', type=str, action='store', required=True)
parser.add_argument('--dork', type=str, action='store', required=True)
parser.add_argument('--output', type=str, action='store')
parser.add_argument('--proxy', type=str, action='store')
args = parser.parse_args()

def main(site, dork_file, output=None):
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }
    valid_urls = []
    with open(str(dork_file), 'r') as f:
        dorks = ['inurl:' + line.strip() for line in f]
        sleep(5)
        with requests.Session() as r:
            page = r.get(f'https://duckduckgo.com/html/?q=site:{site} inurl:{dorks}', timeout=5, headers=headers).text
            soup = BeautifulSoup(page, 'html.parser')
            data = soup.find_all("a", class_="result__url", href=True)

    if 'If this persists, please' in page:
        print('Your IP is blocked')
    else:
        for link in data:
            url = link['href']
            o = urllib.parse.urlparse(url)
            d = urllib.parse.parse_qs(o.query)
            valid_urls.append(d['uddg'][0])
    print(valid_urls)
    
    if output == None:
        pass
    elif output != None:
        print('Saving results to file...')
        with open(output + '.txt', 'w') as r:
            r.write(str(valid_urls))
            r.close()

def check_proxy(proxy):
    try:
        res = requests.get('https://ifconfig.me/ip', proxies={'https': f"socks5://{proxy}"}, timeout=3)
        print(f'Proxy: {proxy} Public IP: ' + res.text)
        # Pass Function here
    except Exception as e:
        print('Dead proxy: ' + proxy)
        print('Killing program....')

main(args.url, args.dork, args.output)
