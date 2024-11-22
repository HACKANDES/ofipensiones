from typing import Optional

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyzer = Optional[SentimentIntensityAnalyzer]


def init_egg_analyzer():
    nltk.download("vader_lexicon", download_dir=".")
    global analyzer
    analyzer = SentimentIntensityAnalyzer()


GOOD = 0.4
BAD = -0.4


special_msg = {
    "The Ultimate Sadness": "Oh Casey...",
    "JMeter": "Then the men, having reached a spot where the trees were thinner, came suddenly in sight of the spectacle itself. Four of them reeled, one fainted, and two were shaken into a frantic cry which the mad cacophony of the orgy fortunately deadened. Legrasse dashed swamp water on the face of the fainting man, and all stood trembling and nearly hypnotised with horror.",
    "DOS": "you're trying to say you like DOS better than me, right?",
}


def easter_egg(msg: str) -> str:
    special = special_msg.get(msg)
    if special is not None:
        return special

    r = analyzer.polarity_scores(msg)["compound"]
    if r >= GOOD:
        return "good"
    elif BAD <= r <= GOOD:
        return "neutral"
    else:
        return "bad"
