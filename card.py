# Card class: 
# -*- coding: utf-8 -*-

# This controls a "card" and it's data. Japanese language only!
# Each card has to be shown few times:
#   1) Kanji -> Meaning
#   2) Kanji -> Kana
#   3) Meaning -> Kanji/Kana
#   4) Kana -> Meaning

class Card:

    def __init__(self):
        # Card ID, so we can easiely retrive it in the future
        self.ID = 0
        # Kanji, e.g. 白人
        self.kanji = "NONE"
        # Kana, e.g. はくじん
        self.kana = "NONE"
        # Meaning, e.g. caucasian
        self.meaning = []
        # Mnemo, e.g. White man = caucasian!
        self.mnemo = "NONE"
        # Lesson of the kanji: the difficulty, level or whatever you wanna call
        # this
        self.lesson = 0
        # Learned level of the kanji
        self.level = 0
        # Was the answer correct/wrong?
        self.answer = False
        # Whether the kanji is active for review or not
        self.active = False
        # Type, described further below
        self.type = 0
        # Date with the last answer answers
        self.date = []
        
        # This is for when we show kana and ask for meaning; but there are
        # other words with the same pronunciation
        self.otherSimilar = []
        
    # Sets the card's variables.
    def set_ID(self, ID):
        self.ID = ID
    def set_kana(self, kana):
        self.kana = kana
    def set_kanji(self, kanji):
        self.kanji = kanji
    def set_meaning(self, meaning):
        self.meaning = meaning
    def set_mnemo(self,mnemo):
        self.mnemo = mnemo
    def set_lesson(self,lesson):
        self.lesson = int(lesson)
    def set_level(self, level):
        self.level = level
    def activate(self):
        self.active = True
    def deactivate(self):
        self.active = False
        
    def add_date(self, date):
        self.date = []
        
    # Sets similar cards (that have the same pronunciation)
    def add_similar(self, similar):
        self.otherSimilar.append(similar)
        
    # Set's card's type:
    # 1: All info is here
    # 2: Mnemo is missing
    # 3: Kanji is missing
    # 4: Kanji and mnemo are missing
    def set_type(self):
        if self.type != 0:
            print "WARNING: Type already set, it's ", self.type , "!!"
        elif self.kana == "NONE" or self.meaning == "NONE":
            print "ERROR: Card not set properly, either meaning or kana missing!"
        else:
            if self.kana != "NONE" and self.kanji != "NONE"  and self.meaning != "NONE" and self.mnemo != "NONE":
                self.type = 1
            elif self.kana != "NONE" and self.kanji != "NONE" and self.meaning != "NONE":
                self.type = 2
            elif self.kana != "NONE" and self.meaning != "NONE" and self.mnemo != "NONE":
                self.type = 3
            elif self.kana != "NONE" and self.meaning != "NONE":
                self.type = 4
         
    # Checks if the supplied meaning matches the card
    def check_meaning(self, meaning):
        if meaning.decode('utf8') in [x.decode('UTF8') for x in self.meaning]:
            return True
        elif meaning in self.otherSimilar:
            print "Correct, but this card is for meaning \"", self.meaning, "\"."
            return True
        else:
            return False
     
    # Checks if the supplied kanji matches the card
    def check_kanji(self, kanji):
        if self.kanji == kanji:
            return True
        else:
            return False
        
    # Checks if the supplied kana matches the card
    def check_kana(self, kana):
        if self.kana == kana:
            return True
        else:
            return False
        
    # Prints info about the card!
    def print_info(self):
        print "Kanji    : ", self.kanji
        print "Kana     : ", self.kana
        print "Meaning  : ", self.meaning
        print "Lesson   : ", self.lesson
        print "Level    : ", self.level
        print "Active   : ", self.active
        print "Type     : ", self.type
