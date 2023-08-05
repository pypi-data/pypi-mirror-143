import nltk

__version__ = "0.1.11"
WORDNET = "wordnet"
POINCARE = "poincare"
nltk.download(WORDNET)
nltk.download('stopwords')

def load(vectors:str=WORDNET):
    if vectors==WORDNET:
        from ffast.wordnet.tokeniser import Tokeniser
        return Tokeniser()
    if vectors==POINCARE:
        from ffast.poincare.tokeniser import Tokeniser
        return Tokeniser()    
    raise TypeError(f"{vectors} is an unrecognised choice. Valid choices are: '{WORDNET}' or '{POINCARE}'")