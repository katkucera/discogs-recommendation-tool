import discogs_client
from bs4 import BeautifulSoup as soup
import requests
import json


d = discogs_client.Client('discgos_search_tool')


def parse_url_to_release(url):
    id = int(url.split('/')[-1])

    return d.master(id) if is_master_release(url) else d.release(id).master

def get_related_release_ids(start_releases):
    related_releases = []

    # for each release get array of list ids
    
    for release in start_releases:

        user_lists = get_user_list_parents(release)
        
        related_releases += [get_sibling_releases(list_id) for list_id in user_lists]

    return related_releases
    

# done!
def get_user_list_parents(release):
    user_list_ids = []
    list_divs = []
    
    source = requests.get(release.url).text
    
    page_soup = soup(source, 'html.parser')

    lists_container = page_soup.find('div',{'id':'lists'})
    list_divs = lists_container.findAll('div')

    for list in list_divs:
        list_id = list.a['href'].split('/')[-1]
        user_list_ids.append(list_id)

    return user_list_ids


# working...need to work with Json
def get_sibling_releases(user_list_id):
    sibling_releases = []
    print(user_list_id)
    
    user_list_url = 'https://api.discogs.com/lists/{}'.format(user_list_id)
    try:
        user_list_data = requests.get(user_list_url).json()
        print(user_list_data['name'])
    except ValueError:
        print('Whelp, you found Chris\' Eternity Tank!¯\_(ツ)_/¯')
    
   # print(user_list_data)
   # sibling_releases += requests.get(user_list_url)
    
    return []


def is_master_release(url):
    return True if 'master' in url else False
    
