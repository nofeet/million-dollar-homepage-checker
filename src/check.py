'''Visit every link in the Million Dollar Homepage and print results.'''

from bs4 import BeautifulSoup
import requests


MILLION_DOLLAR_HOMEPAGE_URL = 'http://www.milliondollarhomepage.com/'


class Advertiser(object):

    def __init__(self, top_left_coord, bottom_right_coord, href, title):
        self.top_left_coord = top_left_coord
        self.bottom_right_coord = bottom_right_coord
        self.href = href
        self.title = title

    @property
    def area(self):
        return ((self.bottom_right_coord[0] - self.top_left_coord[0]) *
                (self.bottom_right_coord[1] - self.top_left_coord[1]))


def parse_million_dollar_homepage():
    text = requests.get(MILLION_DOLLAR_HOMEPAGE_URL).text
    soup = BeautifulSoup(text)
    advertiser_tags = soup.find('map').find_all('area')

    advertisers = []
    for tag in advertiser_tags:
        coords = [int(c) for c in tag['coords'].split(',')]
        advertisers.append(Advertiser(coords[:2], coords[2:], tag['href'],
                                      tag['title']))

    return advertisers


def main():
    advertisers = parse_million_dollar_homepage()


if __name__ == '__main__':
    main()
