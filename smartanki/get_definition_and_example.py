from nltk.corpus import wordnet


def get_definition_and_example(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return ("", "")
    definition = synsets[0].definition()
    examples = synsets[0].examples()
    example = examples[0] if examples else ""
    return (definition, example)
