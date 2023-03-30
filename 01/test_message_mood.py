import pytest
from pytest_mock import MockerFixture

from message_mood import predict_message_mood, SomeModel


@pytest.mark.parametrize(
    ["message", "bad_thresholds", "good_thresholds", "value", "result"],
    [
        [
            "Чапаев и пустота",
            0.3,
            0.8,
            0.9,
            "отл",
        ],
        [
            "Вулкан",
            0.2,
            0.8,
            0.1,
            "неуд",
        ],
        [
            "Какое-то предложение",
            0.4,
            0.6,
            0.5,
            "норм",
        ],
        [
            "Какое-то предложение",
            0.4,
            0.6,
            0.6,
            "норм",
        ],
    ],
)
def test_predict_message_mood(
    mocker: MockerFixture,
    message: str,
    bad_thresholds: float,
    good_thresholds: float,
    value: float,
    result: str,
) -> None:
    mocker.patch("message_mood.SomeModel.predict", return_value=value)
    assert predict_message_mood(message, SomeModel(), bad_thresholds, good_thresholds) == result
