'''Visit every link in the Million Dollar Homepage and print results.'''

from collections import Counter
from operator import attrgetter

from bs4 import BeautifulSoup
import grequests
import requests


MILLION_DOLLAR_HOMEPAGE_URL = 'http://www.milliondollarhomepage.com/'
NUM_SIMULT_REQUESTS = 10


class Advertiser(object):

    def __init__(self, top_left_coord, bottom_right_coord, href, title):
        self.top_left_coord = top_left_coord
        self.bottom_right_coord = bottom_right_coord
        self.orig_url = href
        self.title = title

        self.status = None
        self.text = None
        self.elapsed = None
        self.dest_url = None
        self.num_redirects = None

    @property
    def area(self):
        return ((self.bottom_right_coord[0] - self.top_left_coord[0]) *
                (self.bottom_right_coord[1] - self.top_left_coord[1]))

    def process_response(self, response):
        self._response = response
        if response is not None:
            self.status = response.status_code
            self.text = response.content
            self.elapsed = response.elapsed
            self.dest_url = response.url
            self.num_redirects = len(response.history)

    def __nonzero__(self):
        return self._response is not None

    def __str__(self):
        return 'Advertiser(orig_url="%s")' % self.orig_url


def parse_million_dollar_homepage():
    text = requests.get(MILLION_DOLLAR_HOMEPAGE_URL).text
    soup = BeautifulSoup(text)
    advertiser_tags = soup.find('map').find_all('area')

    reqs = []
    advertisers = []
    for tag in advertiser_tags:
        coords = [int(c) for c in tag['coords'].split(',')]
        advertisers.append(Advertiser(coords[:2], coords[2:], tag['href'],
                                      tag['title']))
        reqs.append(grequests.get(tag['href']))

    for (advertiser, response) in zip(advertisers,
                                      grequests.map(reqs, NUM_SIMULT_REQUESTS)):
        advertiser.process_response(response)

    return advertisers


def analyze(advertisers):
    valid_advertisers = [a for a in advertisers if a]
    return {
        'num_errors': len(advertisers) - len(valid_advertisers),
        'status_code_counter': Counter(a.status for a in valid_advertisers),
        'texts': [a.text for a in valid_advertisers],
        'max_elapsed': max(valid_advertisers, key=attrgetter('elapsed')),
        'num_redirects': sum(1 for a in valid_advertisers if a.orig_url != a.dest_url),
        'max_redirects': max(valid_advertisers, key=attrgetter('num_redirects'))
    }


def generate_report(results):
    pass


def main():
    advertisers = parse_million_dollar_homepage()
    results = analyze(advertisers)
    generate_report(results)


if __name__ == '__main__':
    main()
