from smartanki.utils.translator import HuggingFaceTranslator


global _hf_translator
def translater_f():

    _hf_model_name = "Helsinki-NLP/opus-mt-en-ru"
    try:
        _hf_translator = HuggingFaceTranslator(_hf_model_name)
    except (OSError, FileNotFoundError) as e:
        print(f"[⚠] Hugging Face model '{_hf_model_name}' failed to load. "
              f"Make sure the model is downloaded for offline use. Error: {e}")
        _hf_translator = None
    except Exception as e:
        print(f"[⚠] Unexpected error initializing Hugging Face translator: {e}")
        _hf_translator = None
