from duckduckgo_search import DDGS
import re, json, httpx, argparse, random

# User option here, but using command line
parser = argparse.ArgumentParser(description='Use a custom dork list and search a website')
parser.add_argument('--url', type=str, action='store', required=True)
parser.add_argument('--output', type=str, action='store')
parser.add_argument('--proxy', type=str, action='store')
args = parser.parse_args()

def main(url, output=None, proxy=None, headers=None):
    UA = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:111.0) Gecko/20100101 Firefox/111.0']
    valid_urls = []
    if proxy == None:
        print('Performing scan with tor')
        with DDGS(headers=random.choice(UA), timeout=3) as ddgs:
            for data in ddgs.text(url):
                valid_urls.append(data['href'])
    elif proxy != None:
        print('Performing scan...')
        with DDGS(timeout=3) as ddgs:
            for data in ddgs.text(url):
                valid_urls.append(data['href'])
    
    # Saving to files
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



main(args.url, args.output, args.proxy)
