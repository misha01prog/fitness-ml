from app.models import TrainData


class MotivationEngine:
    def __init__(self, last: TrainData, current: TrainData):
        self.last = last
        self.current = current

    def summarize(self) -> list[str]:
        comparison_result = []

        if self.current.pull_ups > self.last.pull_ups:
            comparison_result.append(f"Ты улучшился в максимальном количестве подтягиваний за один подход! "
                                     f"{self.last.pull_ups} -> {self.current.pull_ups}")
        if self.current.push_ups > self.last.push_ups:
            comparison_result.append(f"Ты улучшился в максимальном количестве отжиманий за один подход! "
                                     f"{self.last.push_ups} -> {self.current.push_ups}")
        if self.current.squats > self.last.squats:
            comparison_result.append(f"Ты улучшился в максимальном количестве приседаний за один подход! "
                                     f"{self.last.squats} -> {self.current.squats}")

        if self.current.sum_pullups > self.last.sum_pullups:
            comparison_result.append(f"Рекорд суммы подтягиваний! Новый рекорд: {self.current.sum_pullups}")
        if self.current.sum_pushups > self.last.sum_pushups:
            comparison_result.append(f"Рекорд суммы отжиманий! Новый рекорд: {self.current.sum_pushups}")
        if self.current.sum_squats > self.last.sum_squats:
            comparison_result.append(f"Рекорд суммы приседаний! Новый рекорд: {self.current.sum_squats}")

        return comparison_result
