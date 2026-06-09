def min_max_normalize(scores):

    if not scores:
        return []

    minimum = min(scores)
    maximum = max(scores)

    if maximum == minimum:

        return [
            50
            for _ in scores
        ]

    normalized = []

    for score in scores:

        value = (
            (score - minimum)
            /
            (maximum - minimum)
        ) * 100

        normalized.append(
            round(
                value,
                2
            )
        )

    return normalized