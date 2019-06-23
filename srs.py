# -*- coding: utf-8 -*-
# Spaced Repitition System, basically stolen from Wanikani.  No need for any
# complex algorithm, this should be just a simple algo 

# TODO:
#   * Change the new stage etc. calculation to be based on some "data-based"
#   class, not the card. Clearly, this can be archieved by somehow using the
#   profile
#   * Import some date-checking library and calculate the next review date,
#   append it to the data. 

# TODO:
#   * Algorithm for running the review
#       - Needs to iterate through all the active cards
#       - Show all the card.data combinations per card
#       - The card.data and cards have to be completely random, so probably
#       pre-load to the memmory and randomize the output order
#       - If wrong: set the next date, append the card to the end of the lesson
#       - If right: set the next date, remove from the array

from card import Card
from datamanager import DataManager
import random

class srs:

    def __init__(self, cards, datamanager):
        # Number of hours till the next review, for each of the 9 "level stages".
        #self.stages = [0, 4, 8, 24, 48, 96, 336, 720, 2880]
        self.stages = [0, 12, 24, 48, 96, 124, 336, 720, 2880]
        # Number of max active cards in the 0th stage.
        self.activeN= 10
        # Max number of cards in lesson that are below lvl 4 max to unblock a
        # new lesson
        self.maxreviewcards = 2
        # The review type. Available: "standard", "onelevel"
        self.reviewtype = "standard"

    
    # Calculate the next stage level given the answer.
    # This REALLY needs to be done based on the datamanager class or something
    # else, card contains all the details about the word, but shouldn't contain
    # info about the progress because each card can correspond to a few
    # different "lessons", e.g. kanji->meaning, meaning->kana.
    # FLAG : NEEDS CHANGING!!
    def new_stage(self, card):
        # If correct, progress one level
        if card.answer == True:
            card.level += 1
        # If incorrect and above lvl 4, drop 2 levels.
        elif card.level >= 4:
            card.level -= 2
        # If incorrect and below lvl 1, drop 1 level.
        else:
            card.level -= 1
        self.new_date(card.level)
    
    # New review date based on the new kanji level. Basically check the date
    # now, check the self.stages and apend that many hours, then append this
    # new date to the data.
    def new_date(lvl):
        # This for now is just a dummy.
        now = 4 # (just a dummy)
        now += self.stages[lvl]

    def set_review(self, reviewtype):
        self.reviewtype = reviewtype
    
    # We will run the SRS algo. It will present all the active cards
    def run_srs(self, cards, datamanager, reviewtype):
        if self.reviewtype == "onelevel":
            print "Will start review of level"
            self.review_lesson(cards,datamanager)
        else:
            print "Oh dear, seems like wrong review type... " , reviewtype

#        activecards = []
#        for i in len(cards):
#            if cards[i].active == true:
#                activecards.append(cards[i])
    
    # This will run the review depending on how many cards need to be reviewed.
    # Review will always come before new lessons, it should not be possible to
    # do a lesson when there are outstanding reviews

    def review_lesson(self, cards, datamanager):
        lesson = raw_input("Lesson to review: ")
        activecards = self.get_card_combinations(lesson, cards, datamanager)
        self.review(cards,datamanager,activecards)

    # This should be able to take an array of cards and run a review for these.
    # This should be able to first count the number of required review
    # combiations, somehow make the required combinations and then somehow
    # print the questions/record answers. Good luck...
    def review(self, cards, datamanager, activecards):
        enumerator = 0
        lessons = []
        # First let's decide wat reviews we will do depending on the type of card
        for i in range(len(activecards)):
            if activecards[i].type == 2 or activecards[i].type == 1:
                # Do all
                lessons.append([1,1,1,1])
                enumerator += 4
            if activecards[i].type == 3 or activecards[i].type == 4:
                # Kana to meaning and meaning to kana only, no kanji
                lessons.append([0,0,1,1])
                enumerator += 2
        # Now we must somehow generate a list of items to iterate through.
        combinations = []
        for i in range(len(lessons)):
            for j in range(len(lessons[i])):
                combinations.append([i, j]);
        # Randomize our list of lesson indices
        random.shuffle(combinations)
        # Number of the reviews left in the lesson
        combinations_left = len(combinations)
        # We will use this array to tag correct/wrong answers. The entries are:
        # 0: first review, 1: answered wrong previously, 2: answered correctly
        # only, 3: answered wrong the first time
        combinations_arr = [0]*len(combinations)
        # We will use this for iterator
        i = 0
        # Only leave if we completed all the reviews!
        while combinations_left != 0:
            # For a nicer output...
            import os
            os.system('cls' if os.name == 'nt' else 'clear')
            print "Number of reviews left: ", combinations_left
            # If the type of lesson is switched on and we did not answer correctly yet
            if lessons[combinations[i][0]][combinations[i][1]] == 1 and combinations_arr[i] <= 1:
                # This is going to be ugly. I should probably shove this in a separate function!
                if combinations[i][1] == 0:
                    # Kanji to meaning
                    print activecards[combinations[i][0]].kanji
                    answer  = raw_input("Meaning: ")
                    iscorrect, combinations_arr[i], combinations_left = self.card_check(0, 
                            activecards[combinations[i][0]], answer, combinations_arr[i], combinations_left)
                elif combinations[i][1] == 1:
                    # Kanji to kana
                    print activecards[combinations[i][0]].kanji
                    answer  = raw_input("Kana: ").decode('utf-8')
                    iscorrect, combinations_arr[i], combinations_left = self.card_check(1,
                            activecards[combinations[i][0]], answer, combinations_arr[i], combinations_left)
                elif combinations[i][1] == 2:
                    # Kana to meaning
                    print activecards[combinations[i][0]].kana
                    answer  = raw_input("Meaning: ")
                    iscorrect, combinations_arr[i], combinations_left = self.card_check(2, 
                            activecards[combinations[i][0]], answer, combinations_arr[i], combinations_left)
                elif combinations[i][1] == 3:
                    # Meaning to kanji
#                    print activecards[combinations[i][0]].meaning
                    print ", ".join([x.encode('UTF8') for x in activecards[combinations[i][0]].meaning])
            
                    answer  = raw_input("Kanji: ").decode('utf-8')
                    iscorrect, combinations_arr[i], combinations_left = self.card_check(3, 
                            activecards[combinations[i][0]], answer, combinations_arr[i], combinations_left)
            if i < len(combinations)-1:
                i += 1
            else:
                i = 1

        # Somehow we have to get this info to the datamanager. Perhaps could
        # just convert this into an array of ID's and true/false to be done
        # with this?
        self.process_results(activecards, combinations, combinations_arr, datamanager)
        print activecards
        print combinations
        print combinations_arr

    # Process the results and send to the data manager to deal with I/O
    def process_results(self, activecards, combinations, combinations_arr, dm):
        results = [True]*len(activecards)
        IDs = [-1]*len(activecards)
        for i in range(len(combinations)):
            if combinations_arr[i] == 3:
                results[combinations[i][0]] = results[combinations[i][0]]
            elif combinations_arr[i] == 4:
                results[combinations[i][0]] = False
            else:
                print "ERROR:srs:process_results"
        for i in range(len(activecards)):
            IDs[i] = activecards[i].ID
        dm.take_results(IDs, results)

    # Checks if the review questions was answered correctly. Returns the answer
    # type, and the reviews left.
    # Returns:
    # combinations_arr - answer type:   3-correct first time, 
    #                                   4-correct after nth attempt, 
    #                                   1-wrong answer
    # combinations_left - number of reviews left. Decrements if the answer was
    # correct (combinations_arr == 3 oe 4)
    def card_check(self, combo, activecard, answer, combinations_arr, combinations_left):
        # First get the lesson review nature
        if combo == 0 or combo == 2:
            real = activecard.meaning
        elif combo == 1:
            real = activecard.kana
        elif combo == 3:
            real = activecard.kanji
        if answer in real: 
            print "Correct!"
            # One less combination to iterate through!
            combinations_left -= 1
            if(combinations_arr) == 0:
                # Correct the first time round
                combinations_arr = 3
            else:
                # Was incorrect on the initial attempt
                combinations_arr = 4
            raw_input()
            return True, combinations_arr, combinations_left
        else:
            if combo == 0 or combo == 2:
                print "Wrong! Your answer: ", answer, "should be: ", ", ".join([x.encode('UTF8') for x in real])
            else:
                print "Wrong! Your answer: ", answer, "should be: ", real
            combinations_arr = 1
            raw_input()
            return False, combinations_arr, combinations_left

    # Return cards active for the review.
    # TODO: implement based on last review.
    def get_card_combinations(self,lesson,cards,datamanager):
        activecards = []
        lesson = int(lesson)
        print "will iterate through lesson:",lesson
        for i in range(len(cards)):
            if(cards[i].lesson == lesson):
                activecards.append(cards[i])
                print "Appenfing a card"
        return activecards
