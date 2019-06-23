# Work In Progress
This is work in progress - there's still A LOT of work to be done

# INTRO
PPon is a small terminal app written in python 2.7 for reviewing Japanese
volcab using Spaced Repitition System loosely based on Wanikani. \\
We can add new volcabulary in form of a "card file", and make as many profiles
for any card combinations as needed. \\
The app was written for Japanese volcabulary, but it probably will work for
most other languages. For each card we review kanji-vocab meaning, pronauntiation and
speach part. \\
At least that's how it should work once it's ready.\\

## Installation
To be written

## Running
To be written

## How does it work?
Basically a terminal review of 'cards'. Each card contains Kanji, Kana and a meaning (in English).
Each card has the folowwing 4 review 'tepes':\\
Kanji -> Kana (Can you pronaunce the written word?) \\
Kanji -> Meaning (Can you translate the written word?) \\
Kana -> Meaning (What does the spoken word mean?)\\
Meaning -> Kanji (Can you pronaunce AND write the spoken word?)\\

Each of this modes belongs to one card, but represents a different 'review';
It's important to be able to write, read AND write, something that's missing im
most other apps like Wanikani. Technically there's Kaniwani too (which helps
with speaking) but they are not too well-integrated and they require web
interface.

# CARD FILES
Card files must contain at least 3 pieces of info per line. All pieces of
"data" should be separated by spaces. If there are spaces in one piece of data
needed (e.g. in mnemo), then we can enclose that piece of data in "". The
pieces of data per line are listed and described below:
- Kanji
- Kana
- Meaning
- Mnemo

THIS WILL BE REPLACED WITH .json FORMAT!

# PROFILE FILES
Technically user doesn't need to worry about these; new profiles are generated
or loaded from existing at run-time. These will contain histry-data per card,
e.g. date of last review, date of the next review, the current review level
etc.  All these pieces of data per-card must be separated by a space. Like in
the CARD FILES case, "" enclosure can be used when spaces are needed  within
a data-item. Data items are listed and described below:
- ID
- Kanji
- Level
- Previous review
- Next review

THIS WILL BE REPLACED WITH .json FORMAT!

# Spaced Repitition System (SRS)
The ppon's SRS is based on Wanikani, with a small simplification. The number of
stages and lengths till the next review are the same, but the next stage
penalty for wrong answer is calculated differently.

## Level stages
Below are the level stages with their "next review" times. Exactly the same as
in wanikani (https://knowledge.wanikani.com/wanikani/srs-stages/)
1: Review now
2: Review in 4h
3: Review in 8h
4: Review in 1d
5: Review in 2d
6: Review in 8d
7: Review in 2w
8: Review in 1m
9: review in 4m

## Penalty calculation
If ALL the four review 'modes' are answered correctly, the whole card gets
progressed onto a new level.  If, however, ANY of these 'modes' is answered
incorrectly, the whole card (and therefore all of it's other learning 'modes')
are devolved onto a lower level.  If the Kanji was above above level 5, the
penalty is 2 levels down.
