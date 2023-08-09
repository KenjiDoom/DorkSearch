import re, json, httpx, argparse, random, requests, urllib.parse
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from time import sleep

parser = argparse.ArgumentParser(description='DorkSearch is used for searching hidden endpoints within a domain using a custom list of dorks.')
parser.add_argument('--url', type=str, action='store', help='The url you want to scan', required=True)
parser.add_argument('--dork', type=str, action='store', help='Dork list you want to use, must be .txt file.', required=True)
parser.add_argument('--output', type=str, action='store', help='Output file you want results to be saved to.')
parser.add_argument('--proxy', type=str, action='store', help='Proxy list using a file .txt or individual proxy ex: 10.10.10.10:1080')
args = parser.parse_args()
console = Console()

def main(site, dork_file, proxy_file, output=None):
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }
    valid_urls = []
    proxy_list = check_proxy_type(proxy_file)    
    with open(str(dork_file), 'r') as f:
       dorks = ['inurl:' + line.strip() for line in f]
       for dork in dorks:
        sleep(1)
        proxy = grab_random_proxy(proxy_list)
        if proxy != None:
            console.print('[bold green] Running...')
            page = requests.get(f'https://duckduckgo.com/html/?q=site:{site} inurl:{dork}', proxies={'https': f"socks5://{proxy}"}, headers=headers).text
            sleep(5)
            soup = BeautifulSoup(page, 'html.parser')
            data = soup.find_all("a", class_="result__url", href=True)
        elif proxy == None:
            console.print('[bold green] Running...')
            page = requests.get(f'https://duckduckgo.com/html/?q=site:{site} inurl:{dork}', headers=headers).text
            sleep(5)
            soup = BeautifulSoup(page, 'html.parser')
            data = soup.find_all("a", class_="result__url", href=True)

        if "If this persists, please" in page:
            console.print('Dork is not found', str(dork), stlye='bold red')
        else:
            for link in data:
                url = link['href']
                o = urllib.parse.urlparse(url)
                d = urllib.parse.parse_qs(o.query)
                valid_urls.append(d['uddg'][0])
    
    table = Table(title='Results', show_edge=False, header_style="bold green")
    table.add_column("URL", style="dim")
    table.add_column("DORK", justify="right")

    table.add_row(
        str(valid_urls), str(dork), style="bold yellow"
    )
    console.print(table)
    
    if output == None:
        pass
    elif output != None:
        print('Saving results to file...')
        with open(output + '.txt', 'w') as r:
            r.write(str(valid_urls))
            r.close()

def grab_random_proxy(proxy_list):
    try:
        random_index_number_proxy_list = random.randint(0, len(proxy_list) - 1)
        random_proxy = proxy_list[random_index_number_proxy_list]
        return random_proxy
    except ValueError:
        return None

def check_proxy(proxy):
    try:
        res = requests.get('https://ifconfig.me/ip', proxies={'https': f"socks5://{proxy}"}, timeout=3)
        return proxy
    except Exception as e:
        console.print('[bold red] Dead proxy found: ' + proxy)

def check_proxy_type(proxy):
    valid_proxies = []
    try:
        if proxy == None:
            pass
        elif proxy.endswith('.txt'):
            console.print('[bold blue] Loading proxies...')
            with open(str(proxy), 'r') as proxy:
                proxies = [line.strip() for line in proxy]
                for proxy in proxies:
                    if check_proxy(proxy) == None:
                        pass
                    else:
                        valid_proxies.append(proxy)
        else:
            valid_proxies.append(check_proxy(proxy))
    except FileNotFoundError:
        console.print('[bold red]File not found...')
    return valid_proxies

if __name__ == '__main__':
    main(args.url, args.dork, args.proxy, args.output)


