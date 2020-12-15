import csv
import requests

from bs4 import BeautifulSoup
# from multiprocessing import Pool
from datetime import datetime
from xml.etree.cElementTree import Element, SubElement, ElementTree

# url = 'http://crawler-test.com/'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/53.0.2785.143 Safari/537.36'
}


def get_html(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
        print(r.text)
    if r.status_code == 404:
        print('Страница не существует!')


def get_link(html):
    soup = BeautifulSoup(html, 'lxml')

    try:
        links = [link.get("href") for link in soup("a")
                 if link.get('href') != "#" and link.get('href') != '/']
    except Exception.DoesNotExist:
        links = ''
    return links


def write_csv(data, url):
    split_url = url.split('://')
    f = open(split_url[1]+'.csv', 'w')
    f.close()
    with open(split_url[1]+'.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        for row in data:
            writer.writerow([row])


def sitemap(all_links, url):
    split_url = url.split('://')
    urlset = Element('urlset',
                     xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    count = 0
    while count < len(all_links):
        today = datetime.now().strftime('%Y-%M-%d')
        urls = SubElement(urlset, "url")
        if all_links[count] is None:
            SubElement(urls, "loc").text = url
        elif split_url[0] in all_links[count]:
            SubElement(urls, "loc").text = str(all_links[count])
        else:
            SubElement(urls, "loc").text = url + str(all_links[count])

        SubElement(urls, "lastmod").text = str(today)
        SubElement(urls, "priority").text = "1.00"
        count += 1
    else:
        tree = ElementTree(urlset)
        tree.write(split_url[1]+".xml")
        print('Ваша карта сайта готова!')
        print(count, 'ссылок было найдено')


# def make_all(url):
#     html = get_html(url)
#     links = get_link(html)
#     write_csv(links, url)
#     sitemap(links, url)


def main():
    url = input('enter something: ')
    start = datetime.now()
    all_links = get_link(get_html(url))
    write_csv(all_links, url)
    sitemap(all_links, url)
    # with Pool(4) as p:
    #     p.map(make_all, all_links)
    end = datetime.now()
    total = end - start
    print("--- %s секунд ---" % (total))


if __name__ == '__main__':
    main()
