from hazm import *
import re
# from parsivar import SpellCheck

class Preproccessing:
    def __init__(self, spell_checking=False, lemmatizing=False, stemming=True, modifying_number=True): 
        self.formal_normalizer = Normalizer(
            correct_spacing=True,
            remove_diacritics=True,
            remove_specials_chars=True,
            decrease_repeated_chars=True,
            seperate_mi=True
        )
        self.informal_normalizer = InformalNormalizer()
        self.lemmatizer = Lemmatizer()
        self.stemmer = Stemmer()
        # self.spell_checker = SpellCheck()
        self._is_spell = spell_checking
        self._is_lemmatize = lemmatizing
        self._is_stem = stemming
        self._is_number = modifying_number
        
    def fit(self, text):
        text = self.__normalizer(text)
        if self._is_number:
            text = self.__modify_numbers(text)
        if self._is_spell:
            text = self.__spell_checker(text)
        if self._is_lemmatize:
            text = self.__lemmatize(text)
        if self._is_stem:
            text = self.__stem(text)
        return text
    
    def __normalizer(self, text):
        text = self.formal_normalizer.normalize(text)
        text = self.informal_normalizer.normalize(text)
        str = ""
        for i in range(len(text)):
            text[i] = [text[i][j][0] if len(text[i][j]) != 1 else text[i][j][0] for j in range(len(text[i]))]
            str += " ".join(text[i])
            str += " "
        return str
    
    def __spell_checker(self, text):
        return self.spell_checker.spell_corrector(text)
    
    def __lemmatize(self, text):
        text = text.split(" ")
        text = [self.lemmatizer.lemmatize(i) for i in text]
        return " ".join(text)
    
    def __stem(self, text):
        text = text.split(" ")
        text = [self.stemmer.stem(i) for i in text]
        return " ".join(text)
    
    def __modify_numbers(self, text):
        num = re.compile(r'[-+]?[.\d]*[\d]+[:,.\d]*')
        text = num.sub(r'عدد', text)
        return text