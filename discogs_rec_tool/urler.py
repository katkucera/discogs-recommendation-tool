def open_url(url):
    print(url)


def get_start_urls():
    start_urls = []
    example_url = 'https://www.discogs.com/Ojas-The-Seven-Levels-Of-Man/master/326093'

    for i in range(3):
        invalid = True
        while invalid:
            url = input(f'Enter url {i + 1}: ')
            if url[:23] == example_url[:23] or url == '':
                start_urls.append(url)
                invalid = False
            else:
                print(f'Error: please enter a valid url [{example_url}]')

    return start_urls
