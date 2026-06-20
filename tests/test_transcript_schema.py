import json


with open(
    "data/screening_transcripts/sample_transcript.json",
    "r",
    encoding="utf-8"
) as file:

    transcript = json.load(file)

print("\nTranscript Loaded Successfully\n")

print(
    "Candidate:",
    transcript["candidate_id"]
)

print(
    "Job:",
    transcript["job_id"]
)

print(
    "Segments:",
    len(transcript["segments"])
)