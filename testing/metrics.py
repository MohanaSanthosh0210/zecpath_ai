import statistics


class Metrics:

    @staticmethod
    def average(values):

        values = [v for v in values if isinstance(v, (int, float))]

        if not values:
            return 0

        return round(statistics.mean(values), 2)

    @staticmethod
    def percentage(part, total):

        if total == 0:
            return 0

        return round((part / total) * 100, 2)

    @staticmethod
    def distribution(values):

        distribution = {}

        for value in values:
            distribution[value] = distribution.get(value, 0) + 1

        return distribution