from duckduckgo_search import DDGS
import re, json, httpx, argparse

# User option here, but using command line
parser = argparse.ArgumentParser(description='Use a custom dork list and search a website')
parser.add_argument('--url', type=str, action='store')
args = parser.parse_args()

def main(url):
    print('Performing scan...')
    with DDGS(timeout=3) as ddgs:
        for r in ddgs.text(url):
            print(r['href'])
main(args.url)

