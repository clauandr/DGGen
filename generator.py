#!/usr/bin/env python3

import csv
import datetime
from random import randint, shuffle, choice, sample
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import argparse

TEXT_COLOR = (0, .1, .5)
DEFAULT_FONT = 'Special Elite'

MONTHS = ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
          'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')

PROFESSIONS = [
    'Anthropologist',
    'Business Executive',
    'Computer Science',
    'Criminal',
    'Engineer',
    'Federal Agent',
    'Firefighter',
    'Foreign Service Officer',
    'Historian',
    'Intelligence Analyst',
    'Intelligence Case Officer',
    'Lawyer',
    'Marine',
    'Media Specialist',
    'Nurse',
    'Paramedic',
    'Physician',
    'Pilot',
    'Police Officer',
    'Program Manager',
    'Sailor',
    'Scientist',
    'Soldier',
    'Special Operator',
]

# Read names and places
with open('data/boys1986.txt') as f:
    MALES = f.read().splitlines()

with open('data/girls1986.txt') as f:
    FEMALES = f.read().splitlines()

with open('data/surnames.txt') as f:
    SURNAMES = f.read().splitlines()

with open('data/towns.txt') as f:
    TOWNS = f.read().splitlines()

DISTINGUISHING = {}
with open('data/distinguishing-features.csv') as distinguishing:
    for row in csv.DictReader(distinguishing):
        for value in range(int(row['from']), int(row['to']) + 1):
            DISTINGUISHING.setdefault(
                (row['statistic'], value), []).append(row['distinguishing'])

class Need2KnowCharacter(object):

    statpools = (
        [13, 13, 12, 12, 11, 11],
        [15, 14, 12, 11, 10, 10],
        [17, 14, 13, 10, 10, 8],
    )

    def __init__(self, gender='male', profession='', bonus_package=''):

        # Hold all dictionary
        self.d = {}
        self.bonus_skills = []
        
        if gender == 'male':
            self.d['male'] = 'X'
            self.d['name'] = choice(SURNAMES).upper() + ', ' + choice(MALES)
        else:
            self.d['female'] = 'X'
            self.d['name'] = choice(SURNAMES).upper() + ', ' + choice(FEMALES)
        self.d['profession'] = profession
        self.d['nationality'] = '(U.S.A.) ' + choice(TOWNS)
        self.d['age'] = '%d    (%s %d)' % (randint(24, 55), choice(MONTHS),
            (randint(1, 28)))

        # Spend the Point Pool
        pool = choice(self.statpools)
        shuffle(pool)
        self.d['strength'] = pool[0]
        self.d['constitution'] = pool[1]
        self.d['dexterity'] = pool[2]
        self.d['intelligence'] = pool[3]
        self.d['power'] = pool[4]
        self.d['charisma'] = pool[5]

        # Derived Stats
        self.d['hitpoints'] = int(round((self.d['strength'] +
                                         self.d['constitution']) / 2.0))
        self.d['willpower'] = self.d['power']
        self.d['sanity'] = self.d['power'] * 5
        self.d['breaking point'] = self.d['power'] * 4
        self.d['damage bonus'] = 'DB=%d' % (((self.d['strength'] - 1) >> 2 ) - 2)
        # Default Skills
        self.d['accounting'] = 10
        self.d['alertness'] = 20
        self.d['athletics'] = 30
        self.d['bureaucracy'] = 10
        self.d['criminology'] = 10
        self.d['disguise'] = 10
        self.d['dodge'] = 30
        self.d['drive'] = 20
        self.d['firearms'] = 20
        self.d['first aide'] = 10
        self.d['heavy machinery'] = 10
        self.d['history'] = 10
        self.d['humint'] = 10
        self.d['melee weapons'] = 30
        self.d['navigate'] = 10
        self.d['occult'] = 10
        self.d['persuade'] = 20
        self.d['psychotherapy'] = 10
        self.d['ride'] = 10
        self.d['search'] = 20
        self.d['stealth'] = 10
        self.d['survival'] = 10
        self.d['swim'] = 20
        self.d['unarmed combat'] = 40

        if profession == 'Anthropologist':

            self.d['anthropology'] = 50
            self.d['bureaucracy'] = 40
            self.d['language1'] = 50
            self.d['language2'] = 30
            self.d['history'] = 60
            self.d['occult'] = 40
            self.d['persuade'] = 40
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']
            self.d['bond4'] = self.d['charisma']
            possible = set([
                ('archeology', 40),
                ('humint', 50),
                ('navigate', 50),
                ('ride', 50),
                ('search', 60),
                ('survival', 50),
            ])
            choice1, choice2 = sample(possible, 2)
            self.d[choice1[0]] = choice1[1]
            self.d[choice2[0]] = choice2[1]

        if profession == 'Historian':

            self.d['archeology'] = 50
            self.d['bureaucracy'] = 40
            self.d['language1'] = 50
            self.d['language2'] = 30
            self.d['history'] = 60
            self.d['occult'] = 40
            self.d['persuade'] = 40
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']
            self.d['bond4'] = self.d['charisma']
            possible = set([
                ('anthropology', 40),
                ('humint', 50),
                ('navigate', 50),
                ('ride', 50),
                ('search', 60),
                ('survival', 50),
            ])
            choice1, choice2 = sample(possible, 2)
            self.d[choice1[0]] = choice1[1]
            self.d[choice2[0]] = choice2[1]

        if profession == 'Computer Science' or profession == 'Engineer':

            self.d['computer science'] = 60
            self.d['craft1label'] = 'Electrician'
            self.d['craft1value'] = 30
            self.d['craft2label'] = 'Mechanic'
            self.d['craft2value'] = 30
            self.d['craft3label'] = 'Microelectronics'
            self.d['craft3value'] = 40
            self.d['science1label'] = 'Mathematics'
            self.d['science1value'] = 40
            self.d['sigint'] = 40
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']
            possible = set([
                ('accounting', 50),
                ('bureaucracy', 50),
                ('craft4value', 40),
                ('language1', 40),
                ('heavy machinery', 50),
                ('law', 40),
                ('science3value', 40),
            ])
            choice1, choice2, choice3, choice4 = sample(possible, 4)
            self.d[choice1[0]] = choice1[1]
            self.d[choice2[0]] = choice2[1]
            self.d[choice3[0]] = choice3[1]
            self.d[choice4[0]] = choice4[1]

        if profession == 'Criminal':

            self.d['alertness'] = 50
            self.d['criminology'] = 60
            self.d['dodge'] = 40
            self.d['drive'] = 50
            self.d['firearms'] = 40
            self.d['law'] = 40
            self.d['melee weapons'] = 40
            self.d['persuade'] = 50
            self.d['stealth'] = 50
            self.d['unarmed combat'] = 50
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']
            self.d['bond4'] = self.d['charisma']
            self.d['craft1label'] = 'Locksmithing'
            possible = set([
                ('craft1value', 40),
                ('demolitions', 40),
                ('disguise', 50),
                ('language1', 40),
                ('humint', 50),
                ('navigate', 50),
                ('occult', 50),
                ('pharmacy', 40),
            ])
            choice1, choice2 = sample(possible, 2)
            self.d[choice1[0]] = choice1[1]
            self.d[choice2[0]] = choice2[1]

        if profession == 'Federal Agent':

            self.d['alertness'] = 50
            self.d['bureaucracy'] = 40
            self.d['criminology'] = 50
            self.d['drive'] = 50
            self.d['firearms'] = 50
            self.d['forensics'] = 30
            self.d['humint'] = 60
            self.d['law'] = 30
            self.d['persuade'] = 50
            self.d['search'] = 50
            self.d['unarmed combat'] = 60
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']
            possible = set([
                ('accounting', 60),
                ('computer science', 50),
                ('language1', 50),
                ('heavy weapons', 50),
                ('pharmacy', 50),
            ])
            choice1 = sample(possible, 1)[0]
            self.d[choice1[0]] = choice1[1]

        if profession == 'Firefighter':

            self.d['alertness'] = 50
            self.d['athletics'] = 60
            self.d['craft1label'] = 'Electrician'
            self.d['craft1value'] = 40
            self.d['craft2label'] = 'Mechanic'
            self.d['craft2value'] = 40
            self.d['demolitions'] = 50
            self.d['drive'] = 50
            self.d['first aide'] = 50
            self.d['forensics'] = 40
            self.d['heavy machinery'] = 50
            self.d['navigate'] = 50
            self.d['search'] = 40
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']

        if profession == 'Foreign Service Officer':

            self.d['accounting'] = 40
            self.d['anthropology'] = 40
            self.d['bureaucracy'] = 60
            self.d['language1'] = 50
            self.d['language2'] = 50
            self.d['language3'] = 40
            self.d['history'] = 40
            self.d['humint'] = 50
            self.d['law'] = 40
            self.d['persuade'] = 50
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']

        if profession == 'Intelligence Analyst':

            self.d['anthropology'] = 40
            self.d['bureaucracy'] = 50
            self.d['computer science'] = 40
            self.d['criminology'] = 40
            self.d['language1'] = 50
            self.d['language2'] = 50
            self.d['language3'] = 40
            self.d['history'] = 40
            self.d['humint'] = 50
            self.d['sigint'] = 40
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']

        if profession == 'Intelligence Case Officer':

            self.d['alertness'] = 50
            self.d['bureaucracy'] = 40
            self.d['criminology'] = 50
            self.d['disguise'] = 50
            self.d['drive'] = 40
            self.d['firearms'] = 40
            self.d['language1'] = 50
            self.d['language2'] = 40
            self.d['humint'] = 60
            self.d['sigint'] = 40
            self.d['stealth'] = 50
            self.d['unarmed combat'] = 50
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']

        if profession == 'Lawyer' or profession == 'Business Executive':

            self.d['accounting'] = 50
            self.d['bureaucracy'] = 50
            self.d['humint'] = 40
            self.d['persuade'] = 60
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']
            self.d['bond4'] = self.d['charisma']
            possible = set([
                ('computer science', 50),
                ('criminology', 60),
                ('language1', 50),
                ('law', 50),
                ('pharmacy', 50),
            ])
            choice1, choice2, choice3, choice4 = sample(possible, 4)
            self.d[choice1[0]] = choice1[1]
            self.d[choice2[0]] = choice2[1]
            self.d[choice3[0]] = choice3[1]
            self.d[choice4[0]] = choice4[1]

        if profession == 'Media Specialist':

            self.d['art1value'] = 60
            self.d['history'] = 40
            self.d['humint'] = 40
            self.d['persuade'] = 50
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']
            self.d['bond4'] = self.d['charisma']
            possible = set([
                ('anthropology', 40),
                ('archeology', 40),
                ('art2value', 40),
                ('bureaucracy', 50),
                ('computer science', 40),
                ('criminology', 50),
                ('language1', 40),
                ('law', 40),
                ('military science', 40),
                ('occult', 50),
                ('science1value', 40),
            ])
            choice1, choice2, choice3, choice4, choice5 = sample(possible, 5)
            self.d[choice1[0]] = choice1[1]
            self.d[choice2[0]] = choice2[1]
            self.d[choice3[0]] = choice3[1]
            self.d[choice4[0]] = choice4[1]
            self.d[choice5[0]] = choice5[1]

        if profession == 'Nurse' or profession == 'Paramedic':

            self.d['alertness'] = 40
            self.d['bureaucracy'] = 40
            self.d['first aide'] = 60
            self.d['humint'] = 40
            self.d['medicine'] = 40
            self.d['persuade'] = 40
            self.d['pharmacy'] = 40
            self.d['science1label'] = 'Biology'
            self.d['science1value'] = 40
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']
            self.d['bond4'] = self.d['charisma']
            possible = set([
                ('drive', 60),
                ('forensics', 40),
                ('navigate', 50),
                ('psychotherapy', 50),
                ('search', 60),
            ])
            choice1, choice2 = sample(possible, 2)
            self.d[choice1[0]] = choice1[1]
            self.d[choice2[0]] = choice2[1]

        if profession == 'Physician':

            self.d['bureaucracy'] = 50
            self.d['first aide'] = 60
            self.d['medicine'] = 60
            self.d['persuade'] = 40
            self.d['pharmacy'] = 50
            self.d['science1label'] = 'Biology'
            self.d['science1value'] = 60
            self.d['search'] = 40
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']
            possible = set([
                ('forensics', 50),
                ('psychotherapy', 60),
                ('science2value', 50),
                ('surgery', 50),
            ])
            choice1, choice2 = sample(possible, 2)
            self.d[choice1[0]] = choice1[1]
            self.d[choice2[0]] = choice2[1]

        if profession == 'Pilot' or profession == 'Sailor':

            self.d['alertness'] = 60
            self.d['bureaucracy'] = 30
            self.d['craft1label'] = 'Electrician'
            self.d['craft1value'] = 40
            self.d['craft2label'] = 'Mechanic'
            self.d['craft2value'] = 40
            self.d['navigate'] = 50
            self.d['pilot1'] = 60
            self.d['science1label'] = 'Meteorology'
            self.d['science1value'] = 40
            self.d['swim'] = 40
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']
            possible = set([
                ('language1', 50),
                ('pilot2', 50),
                ('heavy weapons', 50),
                ('military science', 50),
            ])
            choice1, choice2 = sample(possible, 2)
            self.d[choice1[0]] = choice1[1]
            self.d[choice2[0]] = choice2[1]

        if profession == 'Police Officer':

            self.d['alertness'] = 60
            self.d['bureaucracy'] = 40
            self.d['criminology'] = 50
            self.d['drive'] = 50
            self.d['firearms'] = 40
            self.d['first aide'] = 30
            self.d['humint'] = 50
            self.d['law'] = 30
            self.d['melee weapons'] = 50
            self.d['navigate'] = 40
            self.d['persuade'] = 40
            self.d['search'] = 50
            self.d['unarmed combat'] = 60
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']
            possible = set([
                ('forensics', 50),
                ('heavy machinery', 60),
                ('heavy weapons', 50),
                ('ride', 60),
            ])
            choice1 = sample(possible, 1)[0]
            self.d[choice1[0]] = choice1[1]

        if profession == 'Program Manager':

            self.d['accounting'] = 60
            self.d['bureaucracy'] = 60
            self.d['computer science'] = 50
            self.d['criminology'] = 30
            self.d['language1'] = 50
            self.d['history'] = 40
            self.d['law'] = 40
            self.d['persuade'] = 50
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']
            self.d['bond4'] = self.d['charisma']
            possible = set([
                ('anthropology', 30),
                ('art1value', 30),
                ('craft1value', 30),
                ('science1value', 30),
            ])
            choice1 = sample(possible, 1)[0]
            self.d[choice1[0]] = choice1[1]

        if profession == 'Scientist':

            self.d['bureaucracy'] = 40
            self.d['computer science'] = 40
            self.d['science1value'] = 60
            self.d['science2value'] = 50
            self.d['science3value'] = 50
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']
            self.d['bond4'] = self.d['charisma']
            possible = set([
                ('accounting', 50),
                ('craft1value', 40),
                ('language1', 40),
                ('forensics', 40),
                ('law', 40),
                ('pharmacy', 40),
            ])
            choice1, choice2, choice3 = sample(possible, 3)
            self.d[choice1[0]] = choice1[1]
            self.d[choice2[0]] = choice2[1]
            self.d[choice3[0]] = choice3[1]

        if profession == 'Soldier' or profession == 'Marine':

            self.d['alertness'] = 50
            self.d['athletics'] = 50
            self.d['bureaucracy'] = 30
            self.d['drive'] = 40
            self.d['firearms'] = 40
            self.d['first aide'] = 40
            self.d['military science'] = 40
            self.d['milsci label'] = 'Land'
            self.d['navigate'] = 40
            self.d['persuade'] = 30
            self.d['unarmed combat'] = 50
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']
            self.d['bond3'] = self.d['charisma']
            self.d['bond4'] = self.d['charisma']
            possible = set([
                ('artillery', 40),
                ('computer science', 40),
                ('demolitions', 40),
                ('language1', 40),
                ('heavy machinery', 50),
                ('heavy weapons', 40),
                ('search', 60),
                ('sigint', 40),
                ('swim', 60),
            ])
            choice1, choice2, choice3 = sample(possible, 3)
            self.d[choice1[0]] = choice1[1]
            self.d[choice2[0]] = choice2[1]
            self.d[choice3[0]] = choice3[1]

        if profession == 'Special Operator':

            self.d['alertness'] = 60
            self.d['athletics'] = 60
            self.d['demolitions'] = 40
            self.d['firearms'] = 60
            self.d['heavy weapons'] = 50
            self.d['melee weapons'] = 50
            self.d['military science'] = 60
            self.d['navigate'] = 50
            self.d['stealth'] = 50
            self.d['survival'] = 50
            self.d['swim'] = 50
            self.d['unarmed combat'] = 60
            self.d['bond1'] = self.d['charisma']
            self.d['bond2'] = self.d['charisma']

        # bonus points

        possible_bonus_skills = set([
            'accounting',
            'alertness',
            'anthropology',
            'archeology',
            'art1value',
            'artillery',
            'athletics',
            'bureaucracy',
            'computer science',
            'craft1value',
            'criminology',
            'demolitions',
            'disguise',
            'dodge',
            'drive',
            'firearms',
            'first aide',
            'forensics',
            'heavy machinery',
            'heavy weapons',
            'history',
            'humint',
            'law',
            'medicine',
            'melee weapons',
            'military science',
            'navigate',
            'occult',
            'persuade',
            'pharmacy',
            'pilot1',
            'psychotherapy',
            'ride',
            'science1value',
            'search',
            'sigint',
            'stealth',
            'surgery',
            'survival',
            'swim',
            'unarmed combat',
            'language1',
        ])
        
       
        if bonus_package == 'artist' or bonus_package == 'actor' or bonus_package == 'musician':
            self.bonus_skills = set([
                'alertness',
                'craft1value',
                'disguise',
                'persuade',
                'art1value',
                'art2value',
                'art3value',
                'humint',
            ])
        
        if bonus_package == 'athlete':
            self.bonus_skills = set([
                'alertness',
                'athletics',
                'dodge',
                'first aide',
                'humint',
                'persuade',
                'swim',
                'unarmed combat',
            ])
        
        if bonus_package == 'author' or bonus_package == 'editor' or bonus_package == 'journalist':
            self.bonus_skills = set([
                'anthropology',
                'art1value',
                'bureaucracy',
                'history',
                'law',
                'occult',
                'persuade',
                'humint',
            ])
        
        if bonus_package == 'black bag training' or bonus_package == 'blackbag':
        
            l1,v1 = self.setLabelSkill('craft','Electrician')
            l2,v2 = self.setLabelSkill('craft','Locksmithing')
            
            self.bonus_skills = set([
                'alertness',
                'athletics',
                v1,
                v2,
                'criminology',
                'disguise',
                'search',
                'stealth',
            ])
            
        if bonus_package == 'blue-collar worker' or bonus_package == 'bluecollar':
            self.bonus_skills = set([
                'alertness',
                'craft1value',
                'craft2value',
                'drive',
                'fisrt aide',
                'heavy machinery',
                'navigate',
                'search',
            ])
            
        if bonus_package == 'bureaucrat':
            self.bonus_skills = set([
                'accounting',
                'bureaucracy',
                'computer science',
                'criminology',
                'humint',
                'law',
                'persuade',
            ])    
            self.bonus_skills = self.bonus_skills.union(sample(possible_bonus_skills - self.bonus_skills,1))
        
        if bonus_package == 'clergy':
            self.bonus_skills = set([
                'language1',
                'language2',
                'language3',
                'history',
                'humint',
                'occult',
                'persuade',
                'psychotherapy',
            ])
            
        if bonus_package == 'combat veteran' or bonus_package == 'veteran':
            self.bonus_skills = set([
                'alertness',
                'dodge',
                'firearms',
                'first aide',
                'heavy weapons',
                'melee weapons',
                'stealth',
                'unarmed combat',
            ])
                
        if bonus_package == 'computer enthusiast' or bonus_package == 'hacker':
            l1,v1 = self.setLabelSkill('craft','Microelectronics')
            l2,v2 = self.setLabelSkill('science','Mathematics')
            self.bonus_skills = set([
                'computer science',
                'sigint',
                v1,
                v2,
            ])
            self.bonus_skills = self.bonus_skills.union(sample(possible_bonus_skills - self.bonus_skills,4))
        
        
        if bonus_package == 'counselor':
            self.bonus_skills = set([
                'bureaucracy',
                'first aide',
                'language1',
                'humint',
                'law',
                'persuade',
                'psychotherapy',
                'search',
            ])
        
        if bonus_package == 'criminalist':
            self.bonus_skills = set([
                'accounting',
                'bureaucracy',
                'computer science',
                'criminology',
                'forensics',
                'law',
                'pharmacy',
                'search',
            ])
            
        if bonus_package == 'firefighter':
            self.bonus_skills = set([
                'alertness',
                'demolitions',
                'drive',
                'first aide',
                'forensics',
                'heavy machinery',
                'navigate',
                'search',
            ])  
            
        if bonus_package == 'gangster' or bonus_package == 'deep cover':
            self.bonus_skills = set([
                'alertness',
                'criminology',
                'dodge',
                'drive',
                'persuade',
                'stealth',
            ])  
            
            possible = set([
                'athletics',
                'language1',
                'firearms',
                'humint',
                'melee weapons',
                'pharmacy',
                'unarmed combat',
            ])
            self.bonus_skills = self.bonus_skills.union(sample(possible,2))
        
                
        if bonus_package == 'interrogator':
            self.bonus_skills = set([
                'criminology',
                'language1',
                'language2',
                'humint',
                'law',
                'persuade',
                'pharmacy',
                'search',
            ])
            
        if bonus_package == 'liberal arts degree' or bonus_package == 'arts':
            self.bonus_skills = set([
                'art1value',
                'language1',
                'history',
                'persuade',
            ])
            possible = set([
                'anthropology',
                'archeology',
            ])
            self.bonus_skills = self.bonus_skills.union(sample(possible,1))
            self.bonus_skills = self.bonus_skills.union(sample(possible_bonus_skills - self.bonus_skills,3))
            
        if bonus_package == 'military officer' or bonus_package == 'military':
            self.bonus_skills = set([
                'bureaucracy',
                'firearms',
                'history',
                'military science',
                'navigate',
                'persuade',
                'unarmed combat',
            ])
            possible = set([
                'artillery',
                'heavy machinery',
                'heavy weapons',
                'humint',
                'pilot1',
                'sigint',
            ])
            self.bonus_skills = self.bonus_skills.union(sample(possible,1))
            
        if bonus_package == 'mba':
            self.bonus_skills = set([
                'accounting',
                'bureaucracy',
                'humint',
                'law',
                'persuade',
            ])    
            self.bonus_skills = self.bonus_skills.union(sample(possible_bonus_skills - self.bonus_skills,3))
            
        if bonus_package == 'nurse' or bonus_package == 'paramedic' or bonus_package == 'premed' or bonus_package == 'pre-med':
            l,v = self.setLabelSkill('science','Biology')
            self.bonus_skills = set([
                'alertness',
                'first aide',
                'medicine',
                'persuade',
                'pharmacy',
                'psychotherapy',
                'search',
                v,
            ])    
            
        if bonus_package == 'occult investigator' or bonus_package == 'occult' or bonus_package == 'conspiracy theorist' or bonus_package == 'conspiracy':
            self.bonus_skills = set([
                'anthropology',
                'archeology',
                'computer science',
                'criminology',
                'history',
                'occult',
                'persuade',
                'search',
            ])    
            
        if bonus_package == 'outdoorsman':
            self.bonus_skills = set([
                'alertness',
                'athletics',
                'firearms',
                'navigate',
                'ride',
                'search',
                'stealth',
                'survival',
            ])    
            
        if bonus_package == 'photographer':
            l,v = self.setLabelSkill('art','Photography')
            self.bonus_skills = set([
                'alertness',
                'computer science',
                'persuade',
                'search',
                'stealth',
                v,
            ])    
            self.bonus_skills = self.bonus_skills.union(sample(possible_bonus_skills - self.bonus_skills,2))
        
        if bonus_package == 'pilot' or bonus_package == 'sailor':
            l,v = self.setLabelSkill('craft','Mechanic')
            self.bonus_skills = set([
                'alertness',
                'first aide',
                'language1',
                'navigate',
                'pilot1',
                'survival',
                'swim',
                v,
            ])    
            
        if bonus_package == 'police officer' or bonus_package == 'police':
            self.bonus_skills = set([
                'alertness',
                'criminology',
                'drive',
                'firearms',
                'humint',
                'law',
                'melee weapons',
                'unarmed combat',
            ])     
         
        if bonus_package == 'science grad student' or bonus_package == 'science':
            self.bonus_skills = set([
                'bureaucracy',
                'computer use',
                'craft1value'
                'language1',
                'science1value',
                'science2value',
                'science3value',
            ]) 
            possible = set([
                'accounting',
                'forensics',
                'law',
                'pharmacy',
            ])
            self.bonus_skills = self.bonus_skills.union(sample(possible,1))
            
        if bonus_package == 'social worker' or bonus_package == 'social' or bonus_package == 'criminal justice degree':
            self.bonus_skills = set([
                'bureaucracy',
                'criminology',
                'forensics'
                'language1',
                'humint',
                'law',
                'persuade',
                'search',
            ]) 
            
        if bonus_package == 'soldier' or bonus_package == 'marine':
            self.bonus_skills = set([
                'alertness',
                'artillery',
                'athletics'
                'drive',
                'firearms',
                'heavy weapons',
                'military science',
                'unarmed combat',
            ]) 
            
        if bonus_package == 'translator':
            self.bonus_skills = set([
                'anthropology',
                'language1',
                'language2'
                'language3',
                'history',
                'humint',
                'persuade',
            ]) 
            self.bonus_skills = self.bonus_skills.union(sample(possible_bonus_skills - self.bonus_skills,1))
         
        if bonus_package == 'urban explorer':
            self.bonus_skills = set([
                'alertness',
                'athletics',
                'craft1value'
                'law',
                'navigate',
                'persuade',
                'search',
                'stealth',
            ]) 
        
         
        if bonus_package == 'random':
            self.bonus_skills = sample(possible_bonus_skills, 8)    
        
        # apply bonus skills
        for skill in self.bonus_skills:
            #print("BOOST ",skill)
            boost = self.d.get(skill, 0) + 20
            if boost > 80:
                boost = 80
            self.d[skill] = boost

    def setLabelSkill(self,prefix,label):
        for n in range(1,4):
            key = prefix + str(n) + 'label'
            value = prefix + str(n) + 'value'
            if key not in self.d:
                self.d[key] = label
                return key, value
            elif self.d[key] == label:
                return key, value
                    
        return None, None
        
        
        
    def dump(self):
              
        skills = sorted(self.d.keys())
        
        personal = [
            'name',
            'profession',
            'nationality',
            'age',
            'birthday',
            'male',
            'female',
        ]
        
        statistical = [
            'strength',
            'damage bonus',
            'constitution',
            'dexterity',
            'intelligence',
            'power',
            'charisma',
            'hitpoints',
            'willpower',
            'sanity',
            'breaking point',
            'bond1',
            'bond2',
            'bond3',
            'bond4',
        ]
        print("*Character sheet*")
        print("**Personal**")
        for k in personal:
            if k in self.d:
                print(k," ",self.d[k])
                skills.remove(k)
        print("**Statistical**")    
        for k in statistical:
            if k in self.d:
                print(k," ",self.d[k])
                skills.remove(k)
        print("**Skills**")
        for k in skills:
            if k in self.d:
                if k in self.bonus_skills:
                    mark = "*"
                else:
                    mark = ""
                print(k," ",self.d[k],mark)
    
class Need2KnowPDF(object):

    # Location of form fields in Points (1/72 inch). 0,0 is bottom-left
    field_xy = {
        # Personal Data
        'name': (75, 693),
        'profession': (343, 693),
        'nationality': (343, 665),
        'age': (185, 640),
        'birthday': (200, 640),
        'male': (98, 639),
        'female': (76, 639),

        # Statistical Data
        'strength': (136, 604),
        'damage bonus': (555, 200),
        'constitution': (136, 586),
        'dexterity': (136, 568),
        'intelligence': (136, 550),
        'power': (136, 532),
        'charisma': (136, 514),
        'hitpoints': (195, 482),
        'willpower': (195, 464),
        'sanity': (195, 446),
        'breaking point': (195, 428),
        'bond1': (512, 604),
        'bond2': (512, 586),
        'bond3': (512, 568),
        'bond4': (512, 550),

        # Applicable Skill Sets
        'accounting': (200, 361),
        'alertness': (200, 343),
        'anthropology': (200, 325),
        'archeology': (200, 307),
        'art1value': (200, 289),
        'art2value': (200, 281),
        'art3value': (200, 274),
        'art1label': (90, 289),
        'art2label': (90, 281),
        'art3label': (90, 274),
        'artillery': (200, 253),
        'athletics': (200, 235),
        'bureaucracy': (200, 217),
        'computer science': (200, 200),
        'craft1label': (90, 185),
        'craft1value': (200, 185),
        'craft2label': (90, 177),
        'craft2value': (200, 177),
        'craft3label': (90, 169),
        'craft3value': (200, 169),
        'craft4label': (90, 161),
        'craft4value': (200, 161),
        'criminology': (200, 145),
        'demolitions': (200, 127),
        'disguise': (200, 109),
        'dodge': (200, 91),
        'drive': (200, 73),
        'firearms': (200, 54),
        'first aide': (361, 361),
        'forensics': (361, 343),
        'heavy machinery': (361, 325),
        'heavy weapons': (361, 307),
        'history': (361, 289),
        'humint': (361, 270),
        'law': (361, 253),
        'medicine': (361, 235),
        'melee weapons': (361, 217),
        'military science': (361, 199),
        'milsci label': (327, 199),
        'navigate': (361, 163),
        'occult': (361, 145),
        'persuade': (361, 127),
        'pharmacy': (361, 109),
        'pilot1': (361, 91),
        'pilot2': (361, 83),
        'psychotherapy': (361, 54),
        'ride': (521, 361),
        'science1label': (442, 347),
        'science1value': (521, 347),
        'science2label': (442, 340),
        'science2value': (521, 340),
        'science3label': (442, 333),
        'science3value': (521, 333),
        'science4label': (442, 326),
        'science4value': (521, 326),
        'search': (521, 307),
        'sigint': (521, 289),
        'stealth': (521, 270),
        'surgery': (521, 253),
        'survival': (521, 235),
        'swim': (521, 217),
        'unarmed combat': (521, 200),
        'unnatural': (521, 181),
        'language1': (521, 145),
        'language2': (521, 127),
        'language3': (521, 109),
        'skill1': (521, 91),
        'skill2': (521, 73),
        'skill3': (521, 54),
    }

    # Fields that also get a multiplier
    x5_stats = ['strength', 'constitution', 'dexterity', 'intelligence',
                'power', 'charisma']

    def __init__(self, filename='out.pdf', profession_list=None, count_each=None):
        self.filename = filename
        self.c = canvas.Canvas(self.filename)
        # Set US Letter in points
        self.c.setPageSize((612, 792))
        self.c.setAuthor('https://github.com/jimstorch/DGGen')
        self.c.setTitle('Delta Green Agent Roster')
        self.c.setSubject('Pre-generated characters for the Delta Green RPG')
        # Register Custom Fonts
        pdfmetrics.registerFont(TTFont('Special Elite', 'data/SpecialElite.ttf'))
        pdfmetrics.registerFont(TTFont('OCRA', 'data/OCRA.ttf'))
        # If we're passed an optional list of professions
        # build a clickable Table of Contents on page 1
        if profession_list != None and count_each != None:
            self.bookmark('Table of Contents')
            self.c.setFillColorRGB(0, 0, 0)
            self.c.setFont("OCRA", 10)
            now = datetime.datetime.utcnow().isoformat() + "Z"
            self.c.drawString(150, 712, 'DGGEN DTG ' + now)
            self.c.drawString(150, 700, 'CLASSIFIED/DG/NTK//')
            self.c.drawString(150, 688, 'SUBJ ROSTER/ACTIVE/NOCELL/CONUS//')
            top = 650
            count = 0
            for profession in profession_list:
                pagenum = (count * count_each) + 2
                chapter = '{:.<40}'.format(
                    profession) + '{:.>4}'.format(pagenum)
                self.c.drawString(150, top - count * 22, chapter)
                self.c.linkAbsolute(profession, profession,
                    (145, (top - 6) - (count * 22), 470, (top + 18) - (count * 22)))
                count += 1
            chapter = '{:.<40}'.format('Blank Character Sheet Second Page'
                ) + '{:.>4}'.format(pagenum + count_each)
            self.c.drawString(150, top - count * 22, chapter)
            self.c.linkAbsolute('Back Page', 'Back Page',
                (145, (top - 6) - (count * 22), 470, (top + 18) - (count * 22)))
            self.c.showPage()

    def bookmark(self, text):
        self.c.bookmarkPage(text)
        self.c.addOutlineEntry(text, text)

    def font_color(self, r, g, b):
        self.c.setFillColorRGB(r, g, b)

    def draw_string(self, x, y, text):
        self.c.drawString(x, y, str(text))

    def fill_field(self, field, value):
        x, y = self.field_xy[field]
        self.c.drawString(x, y, str(value))

        if field in self.x5_stats:
            self.draw_string(x + 36, y, str(value * 5))
            self.draw_string(x + 72, y, self.distinguishing(field, value))

    def distinguishing(self, field, value):
        return choice(DISTINGUISHING.get((field, value), [""]))

    def add_page(self, character):
        # Add background.  ReportLab will cache it for repeat
        self.c.setFont(DEFAULT_FONT, 11)
        self.font_color(*TEXT_COLOR)
        self.c.drawImage(
            'data/Character Sheet NO BACKGROUND FRONT.jpg', 0, 0, 612, 792)

        for key in character.d:
            self.fill_field(key, character.d[key])

        # Tell ReportLab we're done with current page
        self.c.showPage()

    def save_pdf(self):
        self.bookmark('Back Page')
        self.c.drawImage(
            'data/Character Sheet NO BACKGROUND BACK.jpg', 0, 0, 612, 792)
        self.c.showPage()
        self.c.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("output", help="output file")
    parser.add_argument("-p","--profession", help="profession")
    parser.add_argument("-b","--bonus", help="bonus")
    parser.add_argument("-n","--number", help="number of characters per profession")
    parser.add_argument("-s","--sex", help="sex (m,f,b)")
    parser.add_argument("-i","--index", help="index with bookmarks",action="store_true")
    parser.add_argument("-t","--text", help="text output",action="store_true")
    args = parser.parse_args()
    
    filename = 'DeltaGreenPregen.pdf'
    if(args.output):
        filename = args.output
    
    number = 1    
    if(args.number):
        number = args.number
        
    sex = choice(['m','f'])
    if(args.sex):
        sex = args.sex
        
    profession_list = PROFESSIONS
    if(args.profession):
        profession_list = []
        for prof in PROFESSIONS:
            if args.profession.upper() in prof.upper():
                profession_list.append(prof)
                break

    bonus_package = 'random'
    if(args.bonus):
        bonus_package = args.bonus
    
    
    total = None
    if(args.index):
        total = number
        if(sex == 'b'):
            total = 2*number
        
    print('professions: ',profession_list)
    print('bonus_package: ',bonus_package)
    print('sex: ',sex)
    
    
    p = Need2KnowPDF(filename, profession_list, total)
    for profession in profession_list:
        p.bookmark(profession)
        for x in range(number):
            if(sex == 'f' or sex == 'b'):
                c = Need2KnowCharacter(gender='female', profession=profession, bonus_package = bonus_package)
                p.add_page(c)
                if(args.text):
                    c.dump()
            if(sex == 'm' or sex == 'b'):
                c = Need2KnowCharacter(gender='male', profession=profession, bonus_package = bonus_package)
                p.add_page(c)
                if(args.text):
                    c.dump()
    p.save_pdf()
