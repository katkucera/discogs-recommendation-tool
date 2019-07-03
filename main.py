from discogser import parse_url_to_release, get_related_release_ids
from urler import get_start_urls, open_url
from youtuber import get_youtube_playlist


def run():
    start_urls = get_start_urls()
    start_releases = [parse_url_to_release(url) for url in start_urls]
    related_release_ids = get_related_release_ids(start_releases)
    playlist_url = get_youtube_playlist(related_release_ids)
    open_url(playlist_url)


if __name__ == '__main__':
    run()


# test
# :)
