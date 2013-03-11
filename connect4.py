#!/usr/bin/env python3.3
#coding: utf8

__author__ = "Ahmet Topal"
__copyright__ = "Copyright (C) 2013 Ahmet Topal <ahmet-topal.com>"

__license__ = "CC BY-SA"
__version__ = "1.0.4"

import sys
import random

class Connect4(object):
    def __init__(self):
        # self.opponent     1 || 2
        self.rows           = 6   # 6 ≤ x
        self.cols           = 7   # 7 ≤ x
        self.empty          = '---'
        self.exit           = 'quit'
        self.newline        = 42
        self.errors         = {
            'name': [
                'Ja wie soll ich dich denn nennen?',
                'Du benötigst einen Namen:',
                'Bitte nenn mir doch deinen Namen',
                'Ach wie gut dass niemand weiß, dass du .. - wer bist du eigentlich?'
            ],
            'bots': [
                'BOT',
                'KI'
            ]
        }
        self.pos            = {}
        self.player         = {
            1: {
                'name'      : 'Player 1',
                'marker'    : 'X'
            },
            2: {
                'name'      : 'Player 2',
                'marker'    : 'O'
            }
        }
        self.whois          = random.randint(1, 2)
        
        self.game           = []
        self.cols_filled    = []
        self.latest         = {} # player, position
    
    # check every input for exit
    def checkExit(self, txt):
        if txt == self.exit:
            # close:
            self.error('Ciö')
        else:
            # return string to continue
            return txt
    
    # items = list of menu items to print
    def printMenu(self, items = []):
        for i in range(0, len(items)):
            if i == 0:
                print('---')
            print(items[i])
    
    # reset everything
    def reset(self):
        self.game           = []
        self.cols_filled    = []
        self.latest         = {} # player, position
        
        return True
    
    # new round, if has winner, print winner else print no winner
    def newRound(self, has_winner = False):
        print('---')
        
        if has_winner:
            print('Glückwunsch {0}, du hast soeben gewonnen!'.format(self.player[self.latest['player']]['name']))
        else:
            print('Runde Vorbei, kein Gewinner!')
        
        self.printMenu(['Neue Runde?', '1 - Ja', '2 - Nein'])
        new = self.checkExit(input('>>> '))
        if new.isnumeric():
            if int(new) in [1, 2]:
                if int(new) == 1:
                    # reset
                    self.reset()

                    # build game
                    self.buildGame()

                    # start round
                    self.round()
                elif int(new) == 2:
                    # close:
                    self.error('Ciö')
            else:
                self.error('Nur 1 oder 2 möglich!')
        else:
            self.error('Möglich ist nur die Auswahl von 1 oder 2')
    
    # print error and quit
    def error(self, error):
        sys.exit(error)
    
    # set opponent
    def setOpponent(self, opponent):
        if opponent.isnumeric():
            if int(opponent) in [1, 2]:
                self.opponent = int(opponent)
                return True
            else:
                self.error('Möglich ist nur 1 für Computergegner und 2 für Menschlichergegner')
        else:
            self.error('Möglich ist nur eine Auswahl von 1 oder 2')
    
    # set name of players
    def setName(self, who, name):
        if who in [1, 2]:
            # check name for bot, set other if player has same name as bot
            if (name != '' and who == 1) or (who == 2 and name != self.player[1]['name']):
                self.player[who]['name'] = name
                return True
            else:
                return False
        else:
            self.error('Ein Spieler mit der ID {0} existiert nicht'.format(who))
    
    # set rows
    def setRows(self, rows):
        if rows.isnumeric():
            if int(rows) >= 6:
                self.rows = int(rows)
                return True
            else:
                self.error('Weniger als 6 Reihen nicht möglich!')
        else:
            self.error('Es darf nur eine Zahl >= 6 eingegeben werden')
    
    # set cols
    def setCols(self, cols):
        if cols.isnumeric():
            if int(cols) >= 7:
                self.cols = int(cols)
                return True
            else:
                self.error('Weniger als 7 Spalten nicht möglich!')
        else:
            self.error('Es darf nur eine Zahl >= 7 eingegeben werden')
    
    # calculate diagonal, horizontal and vertical
    def calculate(self):
        self.pos = {
            'n'     : - self.cols,
            'no'    : - (self.cols - 1),
            'o'     : + 1,
            'so'    : + (self.cols + 1),
            's'     : + self.cols,
            'sw'    : + (self.cols - 1),
            'w'     : - 1,
            'nw'    : - (self.cols + 1)
        }
        return True
    
    # start here, first call
    def start(self):
        print('4 Gewinnt')
        print('Copyright (C) 2013 Ahmet Topal <ahmet-topal.com>')        
        self.printMenu([
            'Bitte wähle eine Zahl:',
            '1 - Mensch gegen Computer',
            '2 - Mensch gegen Mensch'
        ])
        self.setOpponent(self.checkExit(input('>>> ')))
        
        self.printMenu(['Dein Name (Spieler 1):'])
        while(self.setName(1, self.checkExit(input('>>> '))) == False):
            print(random.choice(self.errors['name']))
        
        if self.opponent == 1:
            self.setName(2, self.errors['bots'][1] if (self.player[1]['name'].lower() == self.errors['bots'][0].lower()) else self.errors['bots'][0])
            print('\nDer Computer nennt sich {0}'.format(self.player[2]['name']))
        elif self.opponent == 2:
            print('\nDein Name (Spieler 2):')
            while(self.setName(2, self.checkExit(input('>>> '))) == False):
                print(random.choice(self.errors['name']))
        
        self.printMenu(['Spielfeld', '1 - Standart 6x7', '2 - Selber bestimmen'])
        if (self.checkExit(input('>>> ')) == '2'):
            self.printMenu(['Wieviele Zeilen soll das Spiel haben? (min. 6)'])
            self.setRows(self.checkExit(input('>>> ')))
        
            self.printMenu(['Wieviele Spalten soll das Spiel haben? (min. 7)'])
            self.setCols(self.checkExit(input('>>> ')))
        
        # calculate nw, n, no, o, os, s, sw, w
        self.calculate()
        
        # build game
        self.buildGame()
        
        # start round
        self.round()
    
    # build game field
    def buildGame(self):
        for i in range(0, (self.rows * self.cols)):
            self.game.append(self.empty)
        
        return True
    
    # build game field ui
    def buildField(self):        
        line = '|'
        for i in range(0, len(self.game)):
            line += '{0}|'.format(self.game[i].center(len(self.empty), ' '))
            if (i+1) % self.cols == 0:
                print(line)
                line = '|'
        
        cols = '|';
        for i in range(1, self.cols+1):
            cols += '{0}|'.format(str(i).center(len(self.empty), ' '))
        
        print(cols)
    
    # change who is next player
    def changeWhois(self):
        self.whois = 1 if (self.whois == 2) else 2
    
    # one round, one print of game field
    def round(self):        
        # clear screen using prints, because there is no default possibility
        for i in range(0, self.newline):
            print('\n') 
        
        # build field
        self.buildField()
        
        # new round if game has winner 
        if self.has_winner():
            self.newRound(True)
        
        # new round if cols_filled count = cols count => every col is filled
        if len(self.cols_filled) == self.cols:
            self.newRound(False)
        
        if self.opponent == 1 and self.whois == 2:
            # computer action
            step = self.brain()
        else:
            # user action
            step = self.checkExit(input('\n{0} an der Reihe:\nWähle bitte eine Zahl, um dein "{1}" zu positionieren:\n>>> '.format(self.player[self.whois]['name'], self.player[self.whois]['marker'])))
            
            while step.isnumeric() == False:
                print('Bitte eine Zahl zwischen 1 und {0} wählen!'.format(self.cols))
                step = self.checkExit(input('\n{0} an der Reihe:\n>>> Wähle bitte eine Zahl, um dein "{1}" zu positionieren: '.format(self.player[self.whois]['name'], self.player[self.whois]['marker'])))
            
            while step.isnumeric() and int(step) > self.cols:
                print('Nur eine Zahl zwischen 1 und {0} möglich!'.format(self.cols))
                step = self.checkExit(input('\n{0} an der Reihe:\n>>> Wähle bitte eine Zahl, um dein "{1}" zu positionieren: '.format(self.player[self.whois]['name'], self.player[self.whois]['marker'])))
            
            while step.isnumeric() and int(step) in self.cols_filled:
                print('{0} schon vollständig besetzt'.format(self.cols_filled))
                step = self.checkExit(input('\n{0} an der Reihe:\n>>> Wähle bitte eine Zahl, um dein "{1}" zu positionieren: '.format(self.player[self.whois]['name'], self.player[self.whois]['marker'])))
        
        # position
        step = int(step)
        position = len(self.game) - (self.cols - (step-1))
        
        while self.game[position] != self.empty:
            position -= self.cols
        else:
            # is in first line, so its the highest disc, so row is filled
            if position < self.cols:
                self.cols_filled.append(step)
            
            # set marker in field
            self.game[position] = self.player[self.whois]['marker']
            
        # set latest things
        self.latest['player'] = self.whois
        self.latest['position'] = position
        
        # change whois to other player 1 <=> 2
        self.changeWhois()
        
        # new round
        self.round()
    
    # check if there is a winner with latest marker 
    def has_winner(self, latest = {}):
        # if there is not latest player, latest position set, thats the beginning
        if len(latest) == 0:
            latest = self.latest
            
        if len(latest) != 2:
            return False
        
        # d1 = diagonal left top to right bottom
        # d2 = diagonal right top to left bottom
        # h = horizintal
        # d = diagonal
        possible = {
            'd1'    : {'is': 1, 'check': [self.pos['nw'], self.pos['so']]},
            'd2'    : {'is': 1, 'check': [self.pos['no'], self.pos['sw']]},
            'h'     : {'is': 1, 'check': [self.pos['o'], self.pos['w']]},
            'v'     : {'is': 1, 'check': [self.pos['n'], self.pos['s']]}
        }
        
        # marker
        marker = self.player[latest['player']]['marker']
        start = latest['position']
        
        for p in possible:
            for i in possible[p]['check']:
                pos = start + i
                
                while pos != False and pos >= 0 and pos <= len(self.game)-1 and self.game[pos] == marker:
                    possible[p]['is'] += 1
                    
                    if p in ['d1', 'd2']:                        
                        if (pos+1) % self.cols == 0 or pos % self.cols == 0 or pos >= len(self.game)-self.cols or pos <= self.cols:
                            pos = False
                        else:
                            pos += i
                    elif p == 'h':
                        if (pos+1) % self.cols == 0 or pos % self.cols == 0:
                            pos = False
                        else:
                            pos += i
                    elif p == 'v':
                        if pos >= len(self.game)-self.cols or pos <= self.cols:
                            pos = False
                        else:
                            pos += i
                
                if possible[p]['is'] >= 4:
                    # print(p)
                    return True
        
        return False
    
    # the brain, the bot
    def brain(self):
        percentage_me = {}
        percentage_him = {}
        for i in range(1, self.cols+1):
            percentage_me[i] = 0
            percentage_him[i] = 0
        
        if len(self.latest) != 2:
            # select middle:
            return (self.cols+1) // 2
        
        win_me = False
        win_him = False
        
        for step in range(1, self.cols+1):
            if step not in self.cols_filled:
                latest_me = {}
                latest_him = {}
            
                # position
                position = len(self.game) - (self.cols - (step-1))

                while self.game[position] != self.empty:
                    if self.game[position] == self.player[1]['marker']:
                        percentage_him[step] += 1
                    elif self.game[position] == self.player[2]['marker']:
                        percentage_me[step] += 1
                    
                    position -= self.cols
            
                latest_me['player'] = 2
                latest_me['position'] = position
                latest_him['player'] = 1
                latest_him['position'] = position
            
                if self.has_winner(latest_me):
                    win_me = step
                
                if self.has_winner(latest_him):
                    win_him = step
        
        if win_me != False:
            return win_me
        if win_him != False:
            return win_him
        
        sorted_me = sorted(percentage_me.items(), key=lambda item: item[1], reverse = True)
        sorted_him = sorted(percentage_him.items(), key=lambda item: item[1], reverse = True)
        
        if sorted_me[0][1] > sorted_him[0][1]:
            return sorted_me[0][0]
        elif sorted_me[0][1] < sorted_him[0][1]:
            return sorted_him[0][0]
        elif sorted_me[0][1] == sorted_him[0][1]:
            if sorted_me[0][1] == 0:
                rand = random.randint(1, self.cols)
                while rand in self.cols_filled:
                    rand = random.randint(1, self.cols)
                return rand
            else:
                return sorted_me[0][0]

# start new instance of Connect4
c4 = Connect4()
c4.start()