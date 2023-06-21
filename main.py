from bs4 import BeautifulSoup
from urllib.parse import urlparse
from lib.lib import all_links, process_link, normalize_link, is_relative

out_dir = './out'
replace_url = ''


def process_html_content(url, content, encoding):
    wp = BeautifulSoup(content, 'html.parser')
    links = set()
    for link_elem in wp.find_all('a'):
        link_str = link_elem.get('href')
        # print(orig_link)
        n = urlparse(normalize_link(url, link_str))

        # only grap same origin htmls:
        print(n, url)
        if n.netloc == url.netloc:
            links.add(n.geturl())

            # change urls
            if not is_relative(link_str):
                link_elem['href'] = n._replace(netloc=replace_url)

    return (str(wp), list(links))


def process_html_file(link):
    file = link.path

    if file == '' or file[-1] == '/':
        file = '/index.html'

    p = file.split('.')
    if p[-1] != 'html':
        file = '.'.join(p) + '.html'

    return out_dir+'/'+link.netloc+file


def main():

    url = 'https://einv.versoly.page/'

    runner = all_links(url,
                       process_link(
                           'text/html', process_html_content, process_html_file))

    runner()


main()
