import discogs_client
from bs4 import BeautifulSoup as soup
import requests


d = discogs_client.Client('discgos_search_tool')


def parse_url_to_release(url):
    id = int(url.split('/')[-1])
    release = d.release(id)
    return release if is_master_release else release.master


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
    
    source = requests.get(release.master.url).text
    
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

   # This does not work because requests.get returns a .json file...
   # sibling_releases += requests.get(user_list_url)
    
    return []


def is_master_release(url):
    return True if 'master' in url else False
    
