from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-ru-en"
MarianMTModel.from_pretrained(model_name)
MarianTokenizer.from_pretrained(model_name)
