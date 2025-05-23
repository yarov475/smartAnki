from setuptools import setup, find_packages

setup(
    name='smartanki',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'spacy',
        'nltk',
        'requests',
        'pdfplumber',
        'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
            'smartanki=smartanki.main_cli:main'
        ]
    },
    python_requires='>=3.10',
    include_package_data=True,
    description='📘 SmartAnki – Extract CEFR-based vocabulary and generate Anki flashcards from text or PDF.',
    author='Dmitry Yarochkin',
)
