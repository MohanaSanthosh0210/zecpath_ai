from transcripts.transcript_cleaner import clean_transcript
from transcripts.transcript_normalizer import normalize_transcript


sample_text = (
    "Um I I have uh around three years "
    "of Python experience [noise] "
    "and like worked on FastAPI actually"
)

print("\nRAW TRANSCRIPT")
print("-" * 50)
print(sample_text)

cleaned = clean_transcript(sample_text)

print("\nCLEANED TRANSCRIPT")
print("-" * 50)
print(cleaned)

normalized = normalize_transcript(cleaned)

print("\nNORMALIZED TRANSCRIPT")
print("-" * 50)
print(normalized)