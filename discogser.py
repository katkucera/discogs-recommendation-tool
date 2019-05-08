def parse_url_to_release(url):
    return {}


def get_user_list_parents(release_id):
    return []


def get_related_release_ids(start_releases):
    related_releases = []

    for release in start_releases:
        release_id = release['id']

        user_lists = get_user_list_parents(release_id)
        related_releases += [get_sibling_releases(release_id, user_list['id']) for user_list in user_lists]

    return related_releases


def get_sibling_releases(release_id, user_list_id):
    return []
