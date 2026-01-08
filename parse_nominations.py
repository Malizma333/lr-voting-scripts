import csv
from typing import TypedDict
import random
import utils


class Nomination(TypedDict):
    tracks: list[str]
    commentary: str
    feedback: str


NOMINATION_PATH = "Track-Nominations-Form-2025.csv"
CUTOFF = 30

nomination_data: list[Nomination] = []
nomination_scores: dict[str, int] = {}
playlist: list[str] = []
non_youtube_links: list[str] = []
commentary_array: list[str] = []
feedback_array: list[str] = []

# Extract nomination data from a csv
with open(NOMINATION_PATH, newline="") as f:
    for row in csv.reader(f, delimiter=","):
        if row[0] == "Time":
            continue

        # Filtering tracks by unique id
        tracks = row[3:13]
        track_ids = []
        for track in tracks:
            track_id = utils.extract_id(track.strip())
            if track_id not in track_ids and track_id != "":
                track_ids.append(track_id)

        nomination_data.append(
            {
                "tracks": track_ids,
                "commentary": row[13],
                "feedback": row[14],
            }
        )

# Tallying nominations and aggregating feedback data
for nomination in nomination_data:
    for index, track_id in enumerate(nomination["tracks"]):
        nomination_scores[track_id] = nomination_scores.get(track_id, 0) + (
            1 << (9 - index)
        )

    if nomination["commentary"].strip() != "":
        commentary_array.append(nomination["commentary"])

    if nomination["feedback"].strip() != "":
        feedback_array.append(nomination["feedback"])

# Filter by tracks that had the minimum amount of nominations needed
sorted_tracks = sorted(nomination_scores.items(), key=lambda x: x[1], reverse=True)
shortlist_tracks = [*sorted_tracks]
if len(shortlist_tracks) > CUTOFF:
    # Tracks that have a score lower than or equal to the cutoff track get removed
    shortlist_tracks = [
        *filter(lambda x: x[1] > shortlist_tracks[CUTOFF][1], shortlist_tracks)
    ]

# Combine tracks into playlist
for track, score in shortlist_tracks:
    if "https://" in track:
        non_youtube_links.append(track)
    else:
        playlist.append(track)

random.shuffle(playlist)
playlist_url = "http://www.youtube.com/watch_videos?video_ids=" + ",".join(playlist)

# Output results
print("# Playlist")
print(playlist_url)
if len(non_youtube_links) != 0:
    print("\n".join(non_youtube_links))

eliminated_reached = False
print(f"\n# Shortlist ({len(shortlist_tracks)})")
for i, (track_id, score) in enumerate(sorted_tracks):
    if not eliminated_reached and i == len(shortlist_tracks):
        print(f"\n# Eliminated ({len(sorted_tracks) - len(shortlist_tracks)})")
        eliminated_reached = True

    print("{:<6} {}".format(score, utils.get_link(track_id)))

print("\n# Nomination Commentary")
print("\n".join(commentary_array))

print("\n# Feedback")
print("\n".join(feedback_array))
