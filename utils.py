import requests_cache
from bs4 import BeautifulSoup, Tag

session = requests_cache.CachedSession("yt_url_fetches")


def extract_yt_meta(url: str):
    """
    Gets the title and author of a youtube video given a valid youtube url
    """
    reqs = session.get(url)
    soup = BeautifulSoup(reqs.text, "html.parser")

    title = soup.find(lambda tag: tag.attrs.get("name") == "title")
    if isinstance(title, Tag):
        title = title.get("content")

    author = soup.find(lambda tag: tag.attrs.get("itemprop") == "author")
    if isinstance(author, Tag):
        author = author.contents[1]
        if isinstance(author, Tag):
            author = author.get("content")

    if title is None or author is None:
        final = url
    else:
        final = f"{title} by {author}"

    aliases = open("aliases", "r").read().split("\n")
    for i in range(0, len(aliases), 2):
        if final == aliases[i]:
            final = aliases[i + 1]

    return final


def extract_id(url: str):
    """
    Extracts the id from a (youtube) video url

    Returns the plain url if the video isn't in youtube format (eg bilibili)
    """
    short_index = url.find("youtu.be/")
    if short_index != -1:
        id_index = short_index + 9
        return url[id_index : id_index + 11]

    long_index = url.find("youtube.com/")
    if long_index != -1:
        video_param = url.find("watch?v=")
        id_index = video_param + 8
        return url[id_index : id_index + 11]

    return url


def get_link(id: str):
    """
    Gets the link of a possible youtube video given an id
    """
    if "https://" in id:
        track_link = id
    else:
        track_link = "http://youtu.be/" + id
    return track_link


def print_list(links: list[tuple[str, int]], cutoff_index: int):
    """
    Prints the list of links ranked with the cutoff taken into account
    """
    last_ranking = (0, -1)
    for i, (track_id, score) in enumerate(links):
        if i == cutoff_index:
            print(f"\n## Eliminated ({len(links) - cutoff_index})")

        if score == last_ranking[1]:
            ranking = last_ranking[0] + 1
        else:
            ranking = i + 1
            last_ranking = (i, score)

        print("{} {}".format(f"{ranking})", extract_yt_meta(get_link(track_id))))
