.PHONY: nominations
nominations:
	python3 parse_nominations.py > result_noms.md

.PHONY: votes
votes:
	python3 parse_votes.py > result_votes.md