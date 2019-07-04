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
        
        related_releases += [get_sibling_releases(release_id, user_list['id']) for user_list in user_lists]

    return related_releases


def get_user_list_parents(release):
    user_lists = []

    # page_soup = get_soup(release
    
    return []


def get_sibling_releases(release_id, user_list_id):
    return []


def is_master_release(url):
    return True if 'master' in url else False
    
