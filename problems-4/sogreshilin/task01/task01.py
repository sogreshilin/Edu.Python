import sys
from bs4 import BeautifulSoup
from requests import get
from io import StringIO
from urllib.parse import urlparse


def remove_text_in_brackets(text):
    rv = StringIO()
    open_brackets = ('(', '[', '{')
    close_brackets = (')', ']', '}')
    counters = [0, 0, 0]
    angle_brackets_counter = 0
    for symbol in text:
        if symbol == '<':
            angle_brackets_counter += 1

        if symbol == '>':
            angle_brackets_counter -= 1

        if angle_brackets_counter > 0 and all(counter == 0 for counter in counters):
            rv.write(symbol)
            continue

        try:
            index = open_brackets.index(symbol)
            counters[index] += 1
        except ValueError:
            pass

        try:
            index = close_brackets.index(symbol)
            counters[index] -= 1
            continue
        except ValueError:
            pass

        if all(counter == 0 for counter in counters):
            rv.write(symbol)
    return rv.getvalue()


def is_good_link(tag):
    if tag.name is not 'a':
        return False
    if tag.has_attr('class') and tag['class'] == 'new':
        return False
    if not tag.has_attr('href') or not tag['href'].startswith('/'):
        return False
    return True


def get_first_link(soup):
    for content in soup.find_all('div', attrs={'class': 'mw-parser-output'}):
        for paragraph in content.find_all('p', recursive=False):
            paragraph = BeautifulSoup(remove_text_in_brackets(str(paragraph)), 'lxml').find('p')
            for link in paragraph.find_all(is_good_link):
                return link


def main(scheme, netloc, path):
    visited = list()
    req = get(scheme + '://' + netloc + path)
    while True:
        link = get_first_link(BeautifulSoup(req.text, 'lxml'))
        path = link['href']
        url = scheme + '://' + netloc + path
        print(link['title'], url)
        if path in visited:
            break
        visited.append(path)
        req = get(url)


def validate_url(url):
    parsed = urlparse(url)
    if not 'wikipedia' in parsed.netloc:
        raise ValueError('wikipedia page expected')
    return parsed.scheme, parsed.netloc, parsed.path


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('URL of Wikipedia page was expected', file=sys.stderr)
        sys.exit(-1)

    try:
        scheme, netloc, path = validate_url(sys.argv[1])
        main(scheme, netloc, path)

    except ValueError as error:
        print(error, file=sys.stderr)
