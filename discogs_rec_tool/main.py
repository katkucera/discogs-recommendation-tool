from discogser import parse_url_to_release, get_related_release_ids
from urler import get_start_urls, open_url
from youtuber import get_youtube_playlist


def run():

    start_urls = []

    start_urls = get_start_urls()
    # returns array of start_releases as release objects from discogs_client
    start_releases = [parse_url_to_release(url) for url in start_urls]
    playlist_url = get_youtube_playlist(related_release_ids)

    related_release_ids = get_related_release_ids(start_releases)


    open_url(playlist_url)


if __name__ == '__main__':
    run()


# one more test...
# last one I promise!!!!
# :)
