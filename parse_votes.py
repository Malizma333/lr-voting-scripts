import csv
import utils

voting_data: list[list[tuple[int, str]]] = []
voting_scores: dict[str, int] = {}
feedback_array: list[str] = []
public_lists: list[list[tuple[int, str]]] = []

# Extract voting data from a csv
NUM_TRACKS = 10
with open("Track-Voting-Form-2025.csv", newline="") as f:
    for row in csv.reader(f, delimiter=","):
        if row[0] == "Time":
            continue

        # Filtering tracks by unique id
        tracks = row[3 : 3 + NUM_TRACKS]
        seen = set()
        track_ids: list[tuple[int, str]] = []
        for index, track in enumerate(tracks):
            track_id = utils.extract_id(track.strip())
            if track_id not in seen and track_id != "":
                seen.add(track_id)
                # Preserve index of ranking
                track_ids.append((index, track_id))

        # Add to public lists (list of [index, name], where first item is author name)
        if row[NUM_TRACKS + 3] == "Yes":
            public_lists.append(
                [(-1, row[2]), *map(lambda x: (x[0], utils.get_link(x[1])), track_ids)]
            )

        voting_data.append(track_ids)

        feedback = row[NUM_TRACKS + 4]

        if feedback.strip() != "":
            feedback_array.append(feedback)

# Adding up votes
for vote in voting_data:
    for index, track_id in vote:
        voting_scores[track_id] = voting_scores.get(track_id, 0) + (
            1 << (NUM_TRACKS - 1 - index)
        )

# Sorting tracks by highest vote and combining into playlist
sorted_tracks = sorted(voting_scores.items(), key=lambda x: x[1], reverse=True)
playlist_ids: list[str] = [track[0] for track in sorted_tracks[:NUM_TRACKS]]
playlist_url = "http://www.youtube.com/watch_videos?video_ids=" + ",".join(playlist_ids)

# Output results
print("# Voting Report")

print("\n## Playlist")
print(playlist_url)

print("\n## Scores")
utils.print_list(sorted_tracks, 10)

if len(public_lists) > 0:
    print("\n## Public Lists")
    for ranking in public_lists:
        print(ranking[0][1])
        for index, item in ranking[1:]:
            print(f"{index + 1}) {utils.extract_yt_meta(item)}")
        print()

if len(feedback_array) > 0:
    print("\n## Feedback")
    print("> " + "\n> ".join(feedback_array))
