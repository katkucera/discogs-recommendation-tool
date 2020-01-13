import discogs_client
from authenticator import run_oauth
from discogser import parse_url_to_release, get_related_release_ids
from urler import get_start_urls, open_url
from youtuber import get_youtube_playlist

def run():

    # instatiate client with API key
    d = run_oauth()

    user = d.identity()

    print()
    print(' == User == ')
    print(f'     * username            = {user.username}')
    print(f'     * name                = {user.name}')
    print(' == Access Token == ')
    # print(f'     * oauth_token         = {access_token}')
    # print(f'     * oauth_token_secret = {access_secret}')
    print(' Authentication complete. Future requests will be signed with above tokens.')

    '''
    Application
    '''
    start_urls = []

    start_urls = get_start_urls()
    print(start_urls)

    # returns array of start_releases as release objects from discogs_client
    start_releases = [parse_url_to_release(url) for url in start_urls if url !='']
    print(start_releases)

    # related_release_ids = [get_related_release_ids(release) for release in start_releases]

    # playlist_url = get_youtube_playlist(related_release_ids)

    # open_url(playlist_url)


if __name__ == '__main__':
    run()
