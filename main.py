from duckduckgo_search import DDGS
import re, json, httpx, argparse

# User option here, but using command line
parser = argparse.ArgumentParser(description='Use a custom dork list and search a website')
parser.add_argument('--url', type=str, action='store', required=True)
parser.add_argument('--output', type=str, action='store')
args = parser.parse_args()

def main(url, output=None):
    valid_urls = []
    print('Performing scan...')
    with DDGS(timeout=3) as ddgs:
        for data in ddgs.text(url):
            valid_urls.append(data['href'])
    if output == None:
        pass
    elif output != None:
        print('Saving results to file...')
        with open(output + '.txt', 'w') as r:
            r.write(str(valid_urls))
            r.close()

main(args.url, args.output)


