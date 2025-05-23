import requests

def get_definition_api(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            meaning = data[0]['meanings'][0]
            definition = meaning['definitions'][0]['definition']
            example = meaning['definitions'][0].get('example', '')
            return definition, example
    except Exception as e:
        print(f"API error for {word}: {e}")
    return "", ""
