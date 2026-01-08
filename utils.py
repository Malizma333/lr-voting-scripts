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
