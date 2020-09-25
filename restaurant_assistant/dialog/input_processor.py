from __future__ import annotations
import Levenshtein
from typing import Dict, List, Tuple, Any


MATCH_DIST = 2


def find_keywords(literal_match: Dict[Any, List[str]],
                  help_match: Dict[Any, List[str]],
                  utterance: str) -> List[Tuple[Any, str]]:
    """
    First attempts to find a precise match between a word in the utterance and literal_match.
    If this is not found, the utterance is searched for words in help_match. If these are found,
    the Levenshtein distance is calculated between all words of the utterance and the words in
    literal_match of the matching type. It is matched if a distance is found of less or equal to
    MATCH_DIST.

    :param literal_match: dict mapping type to keywords
    :param help_match: dict mapping type to keywords. Same types as literal_match
    :param utterance: the string to be analyzed
    :return: The matched types and the words they were matched to
    """
    matches = list()
    words = utterance.split()

    for key, keywords in literal_match.items():
        for keyword in keywords:
            if any(word == keyword for word in words):
                matches.append((key, keyword))
                break
        else:
            try:
                help_words = help_match[key]
            except Exception:
                continue

            min_distance = (10, None)
            if any(word in help_words for word in words):
                for literal in literal_match[key]:
                    distance = min([Levenshtein.distance(literal, x) for x in words])

                    if distance < min_distance[0]:
                        min_distance = (distance, literal)

            if min_distance[0] <= MATCH_DIST:
                matches.append((key, min_distance[1]))

    return matches
