import csv
from typing import TypedDict
import utils


class Vote(TypedDict):
    tracks: list[str]
    feedback: str


VOTE_DATA_PATH = "Track-Voting-Form-2025.csv"


voting_data: list[Vote] = []
voting_scores: dict[str, int] = {}
feedback_array: list[str] = []
public_lists: list[list[str]] = []

# Extract voting data from a csv
with open(VOTE_DATA_PATH, newline="") as f:
    for row in csv.reader(f, delimiter=","):
        if row[0] == "Time":
            continue

        # Filtering tracks by unique id
        tracks = row[3:13]
        track_ids: list[str] = []
        for track in tracks:
            track_id = utils.extract_id(track.strip())
            if track_id not in track_ids and track_id != "":
                track_ids.append(track_id)

        if row[13] == "Yes":
            public_lists.append([row[2], *map(utils.get_link, track_ids)])

        voting_data.append({"tracks": track_ids, "feedback": row[14]})

# Adding up votes and aggregating feedback data
for vote in voting_data:
    for index, track_id in enumerate(vote["tracks"]):
        voting_scores[track_id] = voting_scores.get(track_id, 0) + (1 << (9 - index))

    if vote["feedback"].strip() != "":
        feedback_array.append(vote["feedback"])

# Sorting tracks by highest vote and combining into playlist
sorted_tracks = sorted(voting_scores.items(), key=lambda x: x[1], reverse=True)
playlist_ids: list[str] = []
non_youtube_links: list[str] = []

for track in sorted_tracks[:10]:
    if "https://" in track[0]:
        non_youtube_links.append(track[0])
    else:
        playlist_ids.append(track[0])

playlist_url = "http://www.youtube.com/watch_videos?video_ids=" + ",".join(playlist_ids)

# Output results
print("# Playlist")
print(playlist_url)
if len(non_youtube_links) != 0:
    print("\n".join(non_youtube_links))

print("\n# Scores")
for track_id, score in sorted_tracks:
    print("{:<6} {}".format(score, utils.get_link(track_id)))

print("\n# Public Lists")
for ranking in public_lists:
    print(ranking[0])
    for index, item in enumerate(ranking[1:]):
        print(f"{index + 1}) {item}")
    print()

print("\n# Feedback")
print("\n".join(feedback_array))
