# Extracts the id from a (youtube) video url
# Returns the plain url if the video isn't in youtube format (eg bilibili)
def extract_id(url: str):
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


# Gets the link given an id
def get_link(id: str):
    if "https://" in id:
        track_link = id
    else:
        track_link = "http://youtu.be/" + id
    return track_link


# Prints the list of links ranked with the cutoff taken into account
def print_list(links: list[tuple[str, int]], cutoff_index: int):
    last_ranking = (0, -1)
    for i, (track_id, score) in enumerate(links):
        if i == cutoff_index:
            print(f"\n## Eliminated ({len(links) - cutoff_index})")

        if score == last_ranking[1]:
            ranking = last_ranking[0] + 1
        else:
            ranking = i + 1
            last_ranking = (i, score)

        print("{:<3} {:<6} {}".format(f"{ranking})", score, get_link(track_id)))
