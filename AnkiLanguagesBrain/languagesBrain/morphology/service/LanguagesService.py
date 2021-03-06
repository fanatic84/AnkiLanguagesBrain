﻿#-*- coding: utf-8 -*-

from languagesBrain.morphology.db.dao.LanguageDao import *
from languagesBrain.morphology.db.dao.DeckDao import *

from languagesBrain.morphology.db.dto.Language import *

from languagesBrain.morphology.posTagger.Mecab import *
from languagesBrain.morphology.posTagger.stanford.StanfordPosTagger import *

from languagesBrain.morphology.lemmatizer.cst.CstLemmatizer import *

from collections import defaultdict

from languagesBrain.utils.Log import *

class LanguagesService:
    
    def __init__(self, serviceLocator):
        self.serviceLocator = serviceLocator
        self.languageDao = LanguageDao()
        self.deckDao = DeckDao()
        
        self.French = Language(Language.FRENCH, 2, posOptions = {
                "availablePos" : ["A", "ADV", "C", "CL", "D", "ET", "I", "N", "P", "PRO", "V"],
                "activatedPos" : ["A", "ADV", "C", "CL", "D", "ET", "I", "N", "P", "PRO", "V"]
        })
        self.Japanese = Language(Language.JAPANESE, 1, posOptions = {
                "availablePos" : [u'副詞', u'助動詞', u'フィラー', u'動詞', u'名詞', u'形容詞', u'感動詞', u'接続詞', u'接頭詞', u'連体詞'],
                "activatedPos" : [u'副詞', u'助動詞', u'フィラー', u'動詞', u'名詞', u'形容詞', u'感動詞', u'接続詞', u'接頭詞', u'連体詞'],
                "availableSubPos" : [u'一般', u'助詞類接続', u'接尾', u'自立', u'非自立', u'サ変接続', u'ナイ形容詞語幹', u'代名詞', u'副詞可能', u'動詞非自立的', u'固有名詞', u'形容動詞語幹', u'接続詞的', u'数', u'動詞接続', u'名詞接続', u'数接続'],
                "activatedSubPos" : [u'一般', u'助詞類接続', u'接尾', u'自立', u'非自立', u'サ変接続', u'ナイ形容詞語幹', u'代名詞', u'副詞可能', u'動詞非自立的', u'固有名詞', u'形容動詞語幹', u'接続詞的', u'数', u'動詞接続', u'名詞接続', u'数接続']
        })
        self.languagesName = dict({
            #unicode("English", "utf-8")  : Language.ENGLISH,
            unicode("Francais", "utf-8") : Language.FRENCH,
            unicode("日本語", "utf-8")   : Language.JAPANESE
        })
    
    def setupServices(self):
        self.decksService = self.serviceLocator.getDecksService()
    
    def getAvailableLanguageName(self):
        availableLanguageName = []
        for languageName in sorted(self.languagesName, key=self.languagesName.get, reverse=False):
            availableLanguageName.append(languageName)
        return availableLanguageName
    
    def getLanguageNameFromCode(self, code):
        for v,k in self.languagesName.iteritems():
            if k == code :
                return v
        return None
    
    def getCodeFromLanguageName(self, language):
        return self.languagesName[language]
    
    def getLanguageByCode(self, code):
        language = self.languageDao.findLanguageByCode(code)
        if language:
            self.selectPosTagger(language)
        return language
    
    def getLanguageById(self, id):
        language = self.languageDao.findLanguageById(id)
        if language:
            self.selectPosTagger(language)
        return language
    
    def getLanguageByName(self, name):
        language = self.languageDao.findLanguageByCode(self.languagesName[name])
        if language:
            self.selectPosTagger(language)
        return language

    def getPredifinedLanguageByName(self, name):
        languageCode = self.languagesName[name]
        if languageCode == 2:
            return self.French
        elif languageCode == 500:
            return self.Japanese

    def listLanguages(self):
        return self.languageDao.listLanguages()

    def selectPosTagger(self, language):
        if language.posTaggerId == 1:
            language.posTagger = Mecab(language.posOptions)
        elif language.posTaggerId == 2:
            language.posTagger = StanfordPosTagger(language.posOptions)
            language.lemmatizer = CstLemmatizer()

    def addLanguage(self, name):
        
        languageCode = self.languagesName[name]
        if languageCode == 2:
            language = self.French
        elif languageCode == 500:
            language = self.Japanese
        self.selectPosTagger(language)
        return self.languageDao.insertLanguage(language)
    
    def getAllPOS(self, language):
        try:
            return language.posOptions["activatedPos"]
        except Exception: pass
  
    def getAllSubPOS(self, language):
        try:
            return language.posOptions["activatedSubPos"]
        except Exception: pass
    
    def countMorphemes(self, language):
        #FIXME
        language = language
        