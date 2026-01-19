import csv
import random
import utils


nomination_data: list[list[str]] = []
nomination_scores: dict[str, int] = {}
playlist: list[str] = []
non_youtube_links: list[str] = []
commentary_array: list[str] = []
feedback_array: list[str] = []

# Extract nomination data from a csv
NUM_TRACKS = 10
with open("Track-Nominations-Form-2025.csv", newline="") as f:
    for row in csv.reader(f, delimiter=","):
        if row[0] == "Time":
            continue

        # Filtering tracks by unique id
        tracks = row[3 : 3 + NUM_TRACKS]
        track_ids = []
        for track in tracks:
            track_id = utils.extract_id(track.strip())
            if track_id not in track_ids and track_id != "":
                track_ids.append(track_id)

        nomination_data.append(track_ids)

        commentary = row[3 + NUM_TRACKS]
        if commentary.strip() != "":
            commentary_array.append(commentary)

        feedback = row[4 + NUM_TRACKS]
        if feedback.strip() != "":
            feedback_array.append(feedback)


# Adding up nominations
for nomination in nomination_data:
    for index, track_id in enumerate(nomination):
        nomination_scores[track_id] = nomination_scores.get(track_id, 0) + (
            1 << (NUM_TRACKS - 1 - index)
        )

# Filter by tracks that had the minimum amount of nominations needed
sorted_tracks = sorted(nomination_scores.items(), key=lambda x: x[1], reverse=True)
shortlist_tracks = [*sorted_tracks]
CUTOFF = 30
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
print("# Nomination Report")

print("\n## Playlist")
print(playlist_url)
print("Additional:")
if len(non_youtube_links) != 0:
    print("- " + "\n- ".join(non_youtube_links))

print(f"## Shortlist ({len(shortlist_tracks)})")
utils.print_list(sorted_tracks, len(shortlist_tracks))

if len(commentary_array) > 0:
    print("## Commentary")
    print("> " + "\n> ".join(commentary_array))

if len(feedback_array) > 0:
    print("## Feedback")
    print("> " + "\n> ".join(feedback_array))
