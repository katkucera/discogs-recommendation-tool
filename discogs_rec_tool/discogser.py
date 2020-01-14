import requests
import simplejson
import json
import discogs_client
from bs4 import BeautifulSoup as soup


# const variable to represent the ID of the list 'Cris's Eternity Tank' which
# always crashes the program because it can not be called via normal discogs
# api list url...'https://api.discogs.com/lists/{}'.format(list)
CHRIS_LIST = '274428'
CHRIS_MSG = 'Whelp, you found Chris\'s Eternity Tank!¯\\_(ツ)_/¯'

d = discogs_client.Client('discogs_user_list_search_tool')
dot_count = 0
i = 0

def parse_url_to_release(url):
    id_string = url.split('/')[-1]
    id_ = ''.join([i for i in id_string if i.isdigit()])
    print(id_)
    return d.master(id_) if is_master_release(url) else d.release(id_).master


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


# for each release get array of list ids and combine them into related_releases
# returns array of all related_releases.
# TODO: pull only duplicates? figure out what to do with this data
def get_related_release_ids(release):

    user_lists = get_user_list_parents(release)

    print(f'== User lists containing {release.title} ==')
    for list_id in user_lists:
        print(f'       *{list_id.title} ')

    related_releases = [get_sibling_releases(list_id) for list_id in user_lists]

    return related_releases


# TODO: fix this....
def get_sibling_releases(user_list_id):
    # global i
    # user_list_data = {}
    sibling_releases = []
    i = 0

    print(f'== Finding sibling releases from {user_list_id} ==')

    url = f'https://api.discogs.com/lists/{user_list_id}'

    # print(url)
    response = requests.get(url)

    if response.status_code != 200:
        return sibling_releases

    data = response.json()

    print(f'        * json data loaded')

    for release in data['items']:

        if 'id' not in release:
            continue

        sibling_releases.append(release['id'])

        i += 1
        print(i)

    print(f'...sibling releases loaded from {data["name"]}')


    return sibling_releases
    # =================================================================

    # user_list_url = f'https://api.discogs.com/lists/{user_list_id}'
    # # list_file = open(f'list{i}.json', 'w')
    # # i += 1
    # # list_file.write(simplejson.dumps(simplejson.loads(user_list_data), indent=4, sort_keys=True))
    # # list_file.close()
    # try:
    #     user_list_data = requests.get(user_list_url).json()
    #     print(f'        * json data loaded')

    #     for release in user_list_data['items']:
    #         print(release)
    #         try:
    #             sibling_releases.append(release['id'])
    #             # sibling_releases = [release['resource_url'] for release
    #             #     in user_list_data['items']]
    #             print('         * new release added')
    #         except KeyError:
    #             print(f'        * Key error found in {user_list_data["name"]}')
    # # TODO look up exact error for the JSONDecode error I was getting.
    # except ValueError:
    #     msg = CHRIS_MSG if user_list_id == CHRIS_LIST else f'{user_list_id} not reachable.'
    #     print(msg)
    # finally:
    #     print(f'...sibling releases loaded from {user_list_data["name"]}')

    # return sibling_releases

    # ======================================================================


def print_dots():
    pass


#M Make sure release id is from the master release to get info on all possible
# lists.
def is_master_release(url):
    return bool('master' in url)
