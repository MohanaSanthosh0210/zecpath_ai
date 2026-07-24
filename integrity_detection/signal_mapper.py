import json
from pathlib import Path


class SignalMapper:

    BASE_DIR = Path(__file__).resolve().parent

    SIGNAL_FILE = (
        BASE_DIR /
        "config" /
        "malpractice_signals.json"
    )

    @staticmethod
    def load_signals():

        with open(
            SignalMapper.SIGNAL_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def get_signal_names():

        signals = SignalMapper.load_signals()

        return [

            signal["signal"]

            for signal in signals["behavioral_signals"]

        ]


if __name__ == "__main__":

    print(

        SignalMapper.get_signal_names()

    )