import requests
import simplejson
import json
import discogs_client
from bs4 import BeautifulSoup as soup


# const variable to represent the ID of the list 'Cris's Eternity Tank,' which
# always throws JSONDecode exception.
CHRIS_LIST = '274428'
CHRIS_MSG = 'Whelp, you found Chris\'s Eternity Tank!¯\\_(ツ)_/¯'

d = discogs_client.Client('discogs_user_list_search_tool')


def parse_url_to_release(url):

    id_string = url.split('/')[-1]

    id_ = ''.join([i for i in id_string if i.isdigit()])

    return d.master(id_) if 'master' in url else d.release(id_).master


# Web scrape each release url for the user list urls, there is no way to
# get user list urls from the API
def get_user_list_parents(release):

    print(f' == Finding user list IDs for {release.title}')

    user_list_ids = []
    list_divs = []

    source = requests.get(release.url).text

    page_soup = soup(source, 'html.parser')
    lists_container = page_soup.find('div', {'id':'lists'})
    list_divs = lists_container.findAll('div')

    user_list_ids += [str(list.a['href'].split('/')[-1]) for list in list_divs]

    return user_list_ids


# For each release, get array of list ids and combine them into related_releases.
# Returns array of all related_release ids.
# TODO: pull only duplicates? figure out what to do with this data
def get_related_release_ids(release):

    user_lists = get_user_list_parents(release)

    print(f'== User lists containing "{release.title}" ==')
    for list_id in user_lists:
        print(f'       *{list_id.title()} ')

    related_releases = [get_sibling_releases(list_id) for list_id in user_lists]

    return related_releases


def get_sibling_releases(user_list_id):

    sibling_releases = []
    num_releases = 0

    print(f'== Loading data for list {user_list_id} ==')

    url = f'https://api.discogs.com/lists/{user_list_id}'

    response = requests.get(url)

    if response.status_code != 200:
        print(CHRIS_MSG)
        return sibling_releases

    data = response.json()

    print(f'        * {data["name"]} data loaded ')

    for release in data['items']:
        if 'id' not in release:
            continue
        sibling_releases.append(release['id'])
        num_releases += 1

    print(f'        * Successfully loaded {num_releases} sibling releases')

    return sibling_releases


def print_dots():
    pass
