# smartanki/grammar_check.py
import language_tool_python

def check_grammar(text: str):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    return matches
