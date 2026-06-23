# transcripts/speech_to_text.py

import whisper
from pathlib import Path

MODEL = whisper.load_model("base")


def transcribe_audio(audio_path):

    result = MODEL.transcribe(audio_path)

    return result["text"]


def save_transcript(audio_path):

    transcript = transcribe_audio(audio_path)

    output_dir = Path(
        "transcripts/raw_transcripts"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_dir /
        f"{Path(audio_path).stem}_raw.txt"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(transcript)

    print(
        f"Transcript saved: {output_file}"
    )

    return transcript


if __name__ == "__main__":

    audio_folder = Path(
        "transcripts/raw_audio"
    )

    for audio_file in audio_folder.glob("*.wav"):

        print(
            f"\nProcessing: {audio_file}"
        )

        save_transcript(audio_file)