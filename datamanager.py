# -*- coding: utf-8 -*-
# This will manage the "Data", so read the cards from a card file, read saved
# profile and link the profile to the cards. Thic class should also be able to
# save the data, e.g. save the progress in the current profile.
import io
import datetime
import json
from card import Card

# TODO:
#   * Set the profile: Need to read profile data for each kanji; current level,
#     last review, next review date
#   * Think about the date format: need to include some data about review for
#     each sub-card-lesson.
#       - Maybe there should be a "master level" for the card itself, and level
#         gets only progressed if all sub-card-lessons are correct, but
#         diminished if any of the sub-card-lessons is incorrect?
#         It's meant to be difficult, so let's do that

class DataManager:

    # Inits
    def __init__(self,cards):
        # Card file location
        self.cardFile = "NONE"
        # The number of cards
        self.cardFileLen = 0
        # Profile file location
        self.profileFile = "NONE"
        # The number of saved cards in the profile
        self.profileFileLen = 0
        # Cards
        self.card = []
        # Initialise!
        self.user_init(cards)
        
    # Sets the card and profile files
    def user_init(self,cards):
        print "\nWe will set the card file and profile. Please input: "
        self.set_card_file(raw_input("Card file name: "),cards)
        self.set_profile_file(raw_input("Profile name: "))
        
    # Sets the card file. We will read json format, which will make it easier
    # to add/manipulate more data inputs
    def set_card_file(self, cardFile, cards):
        try:
            with open("cards/"+cardFile) as json_file:
                data = json.load(json_file)
        except:
            print "Could not open file cards/" + cardFile + ", exitting"
            quit()
        # Set the number of cards
        self.cardFileLen = len(data["Lessons"])
        # Iterate through cards and fill the data into memory
        for crd in data["Lessons"]:
            # Append a new card object
            cards.append(Card())
            cards[-1].set_ID(crd['ID'])
            cards[-1].set_kanji(crd['Kanji'])
            cards[-1].set_kana(crd['Kana'])
            cards[-1].set_meaning(crd['Meaning'])
            cards[-1].set_lesson(crd['Lesson'])
            cards[-1].set_type()
        # Set the card file location
        self.cardFile = cardFile
        # Save the cards as an internal data object
        self.card = cards
      
    # Sets the profile file
    # TODO: multiple profile/cards, read jmal
    #       * Make a folder per profile. Each profile-folder shoud contain one
    #         file per card-file
    #       * Read and write json files for the profile, it will save time in
    #         long run...
    def set_profile_file(self, profileFile):
        try:
            fl = io.open("profiles/"+profileFile+".dat", "r", encoding='utf-8')
        except:
            print "Could not open file profiles/" + profileFile + ".dat."
            newProfile = raw_input("Generate new profile (y/Y/yes/Yes, else == no)?: ")
            if newProfile in ["y", "Y", "Yes", "yes", "YES"]:
                print "Generating new profile"
                self.make_profile()
                fl = io.open("profiles/"+self.profileFile+".dat", "r", encoding='utf-8')
            else:
                print "Quitting... "
                quit()
        # Read the lines
        lines = fl.readlines()
        fl.close()
        self.profileFileLen = len(lines)
        # Number of enreies must match. Otherwise not supported yet
        if self.profileFileLen != self.cardFileLen:
            print "ERROR:datamanager:set_profile_file:: unequal number of entries in profile/cards not supported yet"
#            quit()
        # Iterate through the entries and fill the card information
        for line in lines:
            ll = line.strip().split(" ")
            if ll[0] == self.card[int(ll[0])].ID:
                print "ID's match!"
            else:
                print "ID's do not match. profile: ", ll[0], "card: "
#            cards.append(Card())
#            cards[-1].set_ID(ll[0])
#            cards[-1].set_kanji(ll[1])
#            cards[-1].set_kana(ll[2])
#            cards[-1].set_meaning(ll[3])
#            cards[-1].set_type()
        # Save the profile
        self.profileFile = profileFile

    # Here we will update the existing profile file. Be careful, by update we
    # really mean overwrite!  I will (at some point) change this to only update
    # the lines/entries that were changed from last time, but for now we will
    # completely overwrite the file.
    # TODO: Make sure we only update the entries that matter, not all...
    def update_profile_file(self):
        fl = open("profiles/"+self.profileFile+".dat", "w")#, encoding='utf-8')
        for i in range(len(self.card)):
            fl.write("%i %s %i %s %s\n" %(int(self.card[i].ID), self.card[i].kanji.encode('utf8'), self.card[i].level, self.card[i].dateLast, self.card[i].dateNext))

    # Sets the results from lessons: it loads the lesson results per
    # correspoding card ID. It will then assign a new "level" of the card and a
    # new lesson date
    # TODO: Complete as explained above
    def set_results(ID, results):
        for i in range(len(ID)):
            for c in range(len(self.card)):
                if ID[i] == self.card[c].ID:
                    print "Eureka, card found!"
                    card[c].answer = results[i]
                    time = datetime.datetime.now()
                    time = time.strftime("%Y:%m:%d:%H:%M")
                    card.dateLast = time

    # Make a new profile, given the card was already provided
    # TODO: Create a new folder per profile, and a saved progress file for each
    # card input file inside that folder. E.g.m if we have card "minna" and
    # "humanjapanese", then profile should be a folder with two files
    # correspoding to these inputs.
    def make_profile(self):
        filename = raw_input("Enter profile name: ")
        print filename
        fl = open("profiles/"+filename+".dat", "w")#, encoding='utf-8')
        self.profileFile = filename
        print "LEN: ", self.cardFileLen
        for i in range(self.cardFileLen):
            fl.write("%i %s %i\n" %(int(self.card[i].ID), self.card[i].kanji.encode('utf8'), 0))
        fl.close()
