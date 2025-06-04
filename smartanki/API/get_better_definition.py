from nltk.corpus import wordnet as wn


def get_better_definition(word):
    synsets = wn.synsets(word)
    if not synsets:
        return "", ""

    # Prefer nouns > verbs > others
    priority = ['n', 'v', 'a', 'r']
    synsets.sort(key=lambda s: priority.index(s.pos()) if s.pos() in priority else 99)

    definition = synsets[0].definition()
    example = synsets[0].examples()[0] if synsets[0].examples() else ""
    return definition, example
