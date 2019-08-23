import requests, urllib.parse
from pyquery import PyQuery as pq

def fetch_east():

    def generate_text(element):
        for child in element.contents():
            if isinstance(child, str):
                if child.strip():
                    yield child.strip() + '\n'
                continue

            item = doc(child)
            if child.tag == 'h2':
                continue
            elif child.tag == 'ul' and (item.hasClass('move') or item.hasClass('backline')):
                continue

            if child.tag == 'h3':
                for line in generate_text(item):
                    yield '### ' + line.strip() + '\n'

            elif child.tag == 'h4':
                yield '\n' + item.text().strip() + '\n'

            elif child.tag == 'dl':
                k = list(generate_text(item))
                print(k)

            elif item.text().strip():
                print(child.tag)
                yield item.text().strip() + '\n'

    url = 'https://www.jreast.co.jp/ryokaku/01_hen/index.html'
    url = 'https://www.jreast.co.jp/ryokaku/02_hen/01_syo/01_setsu/index.html'
    while True:
        print(url)
        r = requests.get(url)
        r.encoding = 'shift_jis'
        doc = pq(r.text)
        contents = doc('#contents .rowContainer')

        yield from generate_text(contents)
       
        relative_url = doc('.move_next a', contents).attr('href')
        if not relative_url:
            break
        url = urllib.parse.urljoin(url, relative_url)
        break

def main():
    #for text in fetch_east():
    #    print(text, end='')
    #return
    with open('jr_east_ryoki.txt', 'w') as f:
        for text in fetch_east():
            f.write(text)

if __name__ == '__main__':
    main()
