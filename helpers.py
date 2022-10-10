import re


def match_intent(pattern, text):
    """ Check patterns """
    result = re.match(rf'{pattern}', text)
    return result is not None
