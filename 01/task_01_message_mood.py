class SomeModel:
    def predict(self, message: str) -> float:
        return (sum(map(ord, list(message))) % 10) / 10  # pragma: no cover


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    predict = model.predict(message)
    if predict < bad_thresholds:
        return "неуд"
    if predict > good_thresholds:
        return "отл"
    return "норм"
