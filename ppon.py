# -*- coding: utf-8 -*-
from card import Card
from datamanager import DataManager
from srs import srs

cards = []

#cards.append(Card())
#cards.append(Card())
#
#cards[1].setKanji("白人")
#cards[1].setKana("はくじん")
#cards[1].setMeaning("caucasian")
#for i in range(len(cards)):
#    print "\nCARD",i,"INFO:"
#    cards[i].printInfo()


# TODO: Everything


dm = DataManager(cards)

for i in range(len(cards)):
    print "\nCARD",i,"INFO:"
    cards[i].print_info()

lesson = srs(cards, dm)
lesson.set_review("onelevel")
lesson.run_srs(cards, dm, "onelevel")

