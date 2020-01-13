import requests
import json
import discogs_client
from bs4 import BeautifulSoup as soup


# const variable to represent the ID of the list 'Cris's Eternity Tank' which
# always crashes the program because it can not be called via normal discogs
# api list url...'https://api.discogs.com/lists/{}'.format(list)
CHRIS_LIST = '274428'
CHRIS_MSG = 'Whelp, you found Chris\'s Eternity Tank!¯\\_(ツ)_/¯'

d = discogs_client.Client('discogs_user_list_search_tool')


def parse_url_to_release(url):
    id_string = url.split('/')[-1]
    id_ = ''.join([i for i in id_string if i.isdigit()])
    print(id_)
    return d.master(id_) if is_master_release(url) else d.release(id_).master


# Web scrape each release url for the user list urls, there is no way to
# get user list urls from the API
def get_user_list_parents(release):
    print(' == Finding user list IDs ==')
    user_list_ids = []
    list_divs = []

    source = requests.get(release.url).text

    page_soup = soup(source, 'html.parser')

    lists_container = page_soup.find('div',{'id':'lists'})
    list_divs = lists_container.findAll('div')

    user_list_ids += [str(list.a['href'].split('/')[-1]) for list in list_divs]
    print(user_list_ids)

    return user_list_ids


# for each release get array of list ids and combine them into related_releases
# returns array of all related_releases.
# TODO: pull only duplicates? figure out what to do with this data
def get_related_release_ids(release):

    user_lists = get_user_list_parents(release)

    related_releases = [get_sibling_releases(list_id) for list_id in user_lists]

    return related_releases


# TODO: fix this....
def get_sibling_releases(user_list_id):
    user_list_data = {}
    sibling_releases = []
    print(user_list_id)

    user_list_url = 'https://api.discogs.com/lists/{}'.format(user_list_id)
    try:
        user_list_data = requests.get(user_list_url).json()
        print(str(user_list_data['name']))
        # with open(user_list_data['name'] + 'data.json', 'w') as fp:
        #     json.dump(user_list_data, fp)
        try:
            sibling_releases = [release['resource_url'] for release
                in user_list_data['items']]
        except KeyError:
            print("Key error found " + user_list_data['name'])
    # TODO look up exact error for the JSONDecode error I was getting.
    except ValueError:
        msg = CHRIS_MSG if user_list_id == CHRIS_LIST else '{} not reachable.'.format(user_list_id)
        print(msg)
        return sibling_releases


    #try:
    #     print(str(user_list_data['name']))
    # except KeyError:
    #     print('Key error found')
    # for release in user_list_data['items']:
    #     try:
    #         sibling_releases.add(release['uri'])
    #     except KeyError:
    #         print("Key error found.")

   # print(user_list_data)
   # sibling_releases += requests.get(user_list_url)

    return sibling_releases


#M Make sure release id is from the master release to get info on all possible
# lists.
def is_master_release(url):
    return bool('master' in url)
