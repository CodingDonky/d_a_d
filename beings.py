from pprint import pprint
import json
import numpy as np
import os, sys
# sys.path.append(os.environ['ENV_DIR']+'DaD/jsonFiles/')

with open(os.environ['ENV_DIR']+'resources/jsonFiles/monsters.json') as f:
    data = json.load(f)
#pprint(data) # Prints out all of the Json File


monstNames = []
monstCRs = []

i = 0
for being in data:
    i += 1
    monstNames.append( being["name"] )
    monstCRs.append( being["challenge_rating"] )
num_beings = i


def print_random_monst_data():
    randomMonstIndex = np.random.randint(numMonst);
    pprint(data[randomMonstIndex])
    i = randomMonstIndex

def print_specific_monst_data( index=0 ):
    i = index
    print ('******** '+data[i]['name']+' ******** ')
    print ('________________________________________')
    pprint(data[i])

class Stats(object):
    kind = 'monster'         # class variable shared by all instances

    def __init__( self, name="Zombie" ):

        i = monstNames.index( name )

        self.canSwim = False
        self.canFly = False

        # META INFO
        self.name = data[i]['name']    # instance variable unique to each instance
        self.type = data[i]['type']
        self.subtype = data[i]['subtype']
        self.cr = data[i]['challenge_rating']
        self.alignment = data[i]['alignment']
        self.size = data[i]['size']
        self.index = monstNames.index(self.name)

        # ATTRIBUTES
        self.intelligence = data[i]['intelligence']
        self.wisdom = data[i]['wisdom']
        self.strength = data[i]['strength']
        self.dexterity = data[i]['dexterity']
        self.charisma = data[i]['charisma']
        self.constitution = data[i]['constitution']

        # ARMOR + HEALTH
        self.hit_dice = data[i]['hit_dice']
        self.hit_points = data[i]['hit_points']
        self.armor_class = data[i]['armor_class']

        # WEAKNESSES / RESISTANCES
        self.condition_immunities = data[i]['condition_immunities']
        self.damage_immunities = data[i]['damage_immunities']
        self.damage_resistances = data[i]['damage_resistances']
        self.damage_vulnerabilities = data[i]['damage_vulnerabilities']

        # ANCILLARY
        self.speed = data[i]['speed']
        self.senses = data[i]['senses']
        self.languages = data[i]['languages']
        self.stealth = data[i]['stealth']

        # ACTIONS
        self.num_actions = 0
        self.actions_attack_bonus = []
        self.actions_damage_bonus = []
        self.actions_desc = []
        self.actions_name = []
        self.actions_damage_dice = []
        try: # Not all monsters have actions
            self.num_actions = len(data[i]['actions'])
            self.actions = data[i]['actions']
            for j in range(0,self.num_actions):
                self.actions_attack_bonus.append(self.actions[j]['attack_bonus'])
                self.actions_desc.append(self.actions[j]['desc'])
                self.actions_name.append(self.actions[j]['name'])

                # Some special abilities do not have damage dice
                try:
                    self.actions_damage_dice.append(self.actions[j]['damage_dice'])
                except Exception, e:
                    self.actions_damage_dice.append('0d0')
                # Some special abilities do not have damage bonus
                try:
                    self.actions_damage_bonus.append(self.actions[j]['damage_bonus'])
                except Exception, e:
                    self.actions_damage_bonus.append(0)

        except Exception, e:
            #print repr(e)
            #print self.name+' has NO ACTIONS'
            self.actions = None

        # SPECIAL ABILITIES
        self.num_special_abilities = 0
        self.special_abilities_name = []
        self.special_abilities_desc = []
        self.special_abilities_attack_bonus = []
        try: # Not all monsters have special abilities
            self.num_special_abilities = len(data[i]['special_abilities'])
            self.special_abilities = data[i]['special_abilities']
            for j in range(0,self.num_special_abilities):
                self.special_abilities_name.append(self.special_abilities[j]['name'])
                self.special_abilities_desc.append(self.special_abilities[j]['desc'])
                self.special_abilities_attack_bonus.append(self.special_abilities[j]['attack_bonus'])
        except Exception, e:
            #print repr(e)
            self.special_abilities = None

        if 'fly' in self.speed:
            self.canFly = True
        if 'swim' in self.speed:
            self.canSwim = True

    def perform_random_action(self):
        i = np.random.randint( self.num_actions );

        name = str( self.name )
        actionName = str( self.actions_name[i] )
        actionDesc = str( self.actions_desc[i] )
        attackBonus = int( self.actions_attack_bonus[i] )
        damageBonus = int( self.actions_damage_bonus[i] )

        print('The '+name+' uses its '+actionName)
        print( actionDesc )
        print('')

    def perform_random_special_ability(self):
        if self.num_special_abilities == 0:
            print 'No special abilities!'
            print ''
        else:
            i = np.random.randint( self.num_special_abilities );

            name = str( self.name )
            specialAbilityName = str( self.special_abilities_name[i] )
            specialAbilityDesc = str( self.special_abilities_desc[i] )
            specialAbilityBonus = int( self.special_abilities_attack_bonus[i] )

            print('The '+name+' uses its '+specialAbilityName)
            print( specialAbilityDesc )
            print('')
