import sys, os
import json
import re

POWERS = json.load(open("dndgen/powers.json"))
WEAPONS = json.load(open("dndgen/weapons.json"))


def check_flag(name, flag, default):
    name = re.sub('\[.*?\]', '', name).strip()
    if name in POWERS:
        if flag in POWERS[name]:
            return POWERS[name][flag] == 'yes'
    return default


def charsheet(name):
    return check_flag(name, 'charsheet', True)


def is_utility(name):
    return check_flag(name, 'utility', False)


def get_power_info(name):
    data = {
        "name": name,
        "charsheet": charsheet(name),
        "utility": is_utility(name),
        "title": "",
        "action": "[no]",
        "target": "[no]",
        "vs": "[no]",
        "attack": "[no]",
        "range": "[no]",
        "hit": "[no]",
        "is_weapon": "yes",
        "comment": "",
        "hit_comment": "",
        "type": "[no]"
    }
    name = re.sub('\[.*?\]', '', name).strip()
    if name in POWERS:
        data.update(POWERS[name])
    else:
        print("Power " + name + " not found")
    return data

def get_weapon_info(name):
    data = {
        "name": name,
        "range": "[no]",
        "W": "[no]",
    }
    name = re.sub('\[.*?\]', '', name).strip()
    if name in WEAPONS:
        data.update(WEAPONS[name])
    else:
        print("Weapon " + name + " not found")
    return data


class Converter(object):
    attacks = re.compile('Attacks:(.*)Base Saving throw')
    attack = re.compile('([\w ]*).*?:\s+([0-9d\+\-]+).*vs (\w*).*damage\s+1\[W\]=(([0-9d]+)[0-9d\+\- ]+)')
    talent = re.compile('([\w \']+)')

    def find_attacks(self, data):
        f = self.attacks.search(data.replace('\n', ';NEWLINE;'), re.MULTILINE)
        if f:
            lst = [l.strip() for l in f.groups()[0].replace(';NEWLINE;', '\n').split('\n') if l]
            found_attacks = []
            for attack_str in lst:
                s = self.attack.search(attack_str)
                if s:
                    found_attacks.append(s.groups())
            return found_attacks + [['', '', '', '', ''] for _ in range(4 - len(found_attacks))]


    def find_talents(self, data):
        f = self.attacks.search(data.replace('\n', ';NEWLINE;'), re.MULTILINE)
        if f:
            lst = [l.strip() for l in f.groups()[0].replace(';NEWLINE;', '\n').split('\n') if l]
            found_attacks = []
            for attack_str in lst:
                s = self.attack.search(attack_str)
                if not s:
                    s = self.talent.search(attack_str)
                    if s and not s.groups()[0].startswith('v Versatile') and not s.groups()[0].startswith(
                            'w Weapon') and not s.groups()[0].startswith('i Implement'):
                        found_attacks.append(s.groups()[0].strip())
            return found_attacks


    langs = re.compile('Languages:\s+(.*)')
    def find_languages(self, data):
        s = self.langs.search(data)
        if s:
            lang_lst = [l.strip() for l in s.groups()[0].split(';') if l.strip()]
            return lang_lst + ['' for _ in range(3 - len(lang_lst))]


    rituals = re.compile('Rituals Known:(.*)Skills:')
    ritual = re.compile('(.*)\s+\[(Level \d+)\]')
    def find_rituals(self, data):
        f = self.rituals.search(data.replace('\n', ';NEWLINE;'), re.MULTILINE)
        if f:
            lst = [l.strip() for l in f.groups()[0].replace(';NEWLINE;', '\n').split('\n') if l.strip()]
            found_rituals = []
            for ritual_str in lst:
                s = self.ritual.search(ritual_str)
                if s:
                    found_rituals.append(s.groups())
            return found_rituals + [['', ''] for _ in range(10 - len(found_rituals))]


    feats = re.compile('Feats:(.*)At-Will:')
    def find_feats(self, data):
        f = self.feats.search(data.replace('\n', ';NEWLINE;'), re.MULTILINE)
        if f:
            lst = [l.strip() for l in f.groups()[0].replace(';NEWLINE;', '\n').split('\n') if l.strip()]
            return lst + ['' for _ in range(16 - len(lst))]


    atwills = re.compile('At-Will:(.*)Other Standard Actions:')
    encounters = re.compile('Encounter Powers:(.*)Daily Powers:')
    power = re.compile('(.*):')
    power2 = re.compile('(.*)\s+\[Level (\d+).*\]')
    power3 = re.compile('(.*)')

    def find_power(self, regex, count, utility=False):
        def _find_power(data):
            f = regex.search(data.replace('\n', ';NEWLINE;'), re.MULTILINE)
            if f:
                lst = [l.strip() for l in f.groups()[0].replace(';NEWLINE;', '\n').split('\n') if l.strip()]
                found = []
                for item in lst:
                    s = self.power.search(item)
                    if not s:
                        s = self.power2.search(item)
                    if not s:
                        s = self.power3.search(item)
                    if s:
                        name = s.groups()[0]
                        if name.strip() != 'Channel Divinity' and charsheet(name) and \
                                (utility or not is_utility(name)):
                            found.append(name)
                return found + ['' for _ in range(count - len(found))]

        return _find_power


    def find_dailys(self, data, utility=False):
        f = re.search('Daily Powers:(.*);NEWLINE;%s;NEWLINE;' % self.char['race'], data.replace('\n', ';NEWLINE;'), re.MULTILINE)
        if f:
            lst = [l.strip() for l in f.groups()[0].replace(';NEWLINE;', '\n').split('\n') if l.strip()]
            found = []
            for item in lst:
                s = self.power2.search(item)
                if s:
                    if utility or not is_utility(s.groups()[0]):
                        found.append(s.groups()[0])
            return found + ['' for _ in range(6 - len(found))]


    def find_utility(self, data):
        found = [(item, 'at-will') for item in self.find_power(self.atwills, 0, True)(data) if is_utility(item)]
        found += [(item, 'encounter') for item in self.find_power(self.encounters, 0, True)(data) if is_utility(item)]
        found += [(item, 'daily') for item in self.find_dailys(data, True) if is_utility(item)]
        return found + [('', '') for _ in range(8 - len(found))]


    def find_race_features(self, data):
        f = re.search('Daily Powers:.*%s;NEWLINE;(.*);NEWLINE;%s;NEWLINE;' % (self.char['race'], self.char['class']),
                      data.replace('\n', ';NEWLINE;'), re.MULTILINE)
        if f:
            lst = [l.strip() for l in f.groups()[0].replace(';NEWLINE;', '\n').split('\n') if l.strip()]
            return lst + ['' for _ in range(8 - len(lst))]


    def find_class_features(self, data):
        f = re.search(
            'Daily Powers:.*%s;NEWLINE;(.*);NEWLINE;%s\'s Equipment:;NEWLINE;' % (self.char['class'], self.char['character_name']),
            data.replace('\n', ';NEWLINE;'), re.MULTILINE)
        if f:
            lst = [l.strip() for l in f.groups()[0].replace(';NEWLINE;', '\n').split('\n') if l.strip()]
            return lst + ['' for _ in range(14 - len(lst))]

    def fill(self, char, key, regex, data):
        groups = None
        if hasattr(regex, "__call__"):
            groups = regex(data)
        else:
            val = regex.search(data)
            if val:
                groups = val.groups()
                if len(groups) == 1:
                    groups = groups[0]

        if groups:
            char[key] = groups

    def convert(self, data):
        data = data.replace('\r\n', '\n')
        regexes = {
            "player_name": re.compile('Representing (.*)'),

            "ABILITY": {
                "str": re.compile('Strength\s+(\d+)\s*\(([-\+]\d+)\)'),
                "con": re.compile('Constitution\s+(\d+)\s*\(([-\+]\d+)\)'),
                "dex": re.compile('Dexterity\s+(\d+)\s*\(([-\+]\d+)\)'),
                "int": re.compile('Intelligence\s+(\d+)\s*\(([-\+]\d+)\)'),
                "wis": re.compile('Wisdom\s+(\d+)\s*\(([-\+]\d+)\)'),
                "cha": re.compile('Charisma\s+(\d+)\s*\(([-\+]\d+)\)'),
            },

            "BASIC": {
                "height": re.compile('Height:\s+(\d+\'\s+\d+\")'),
                "weight": re.compile('Weight:\s+(\d+\s+lb)'),
                "scales": re.compile('Scales:\s+(\w+)'),
                "eyes": re.compile('Eyes:\s+(\w+)'),
                "hair": re.compile('Hair:\s+(\w+)'),
                "size": re.compile('Size:\s+(\w+)'),
                "speed": re.compile('Speed:\s+(\d+)'),
                "vision": re.compile('Vision:\s+(.+)\n'),
            },

            "HP": {
                "max_hp": re.compile('Maximum Hit Points:\s+(\d+)'),
                "bloodied": re.compile('Bloodied:\s+(\d+)'),
                "surge_value": re.compile('Surge Value:\s+(\d+)'),
                "surger_day": re.compile('Surges / Day:\s+(\d+)'),
            },

            "initiative_score": re.compile('Initiative:\s+[0-9]*d20\s+([0-9\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
            "Armor": re.compile('Armor:\s+(\w+)'),
            "Shield": re.compile('Shield:\s+(\w+)'),
            "Base Saving throw": re.compile('Base Saving throw:\s+(d\d+ vs \d+)'),
            "Attacks": self.find_attacks,
            "Talents": self.find_talents,
            "Rituals": self.find_rituals,
            "Feats": self.find_feats,
            "Languages": self.find_languages,
            "ATTACK": {
                "str_attack": re.compile('Base Strength Attack:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "dex_attack": re.compile('Base Dexterity Attack:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "con_attack": re.compile('Base Constitution Attack:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "int_attack": re.compile('Base Intelligence Attack:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "wis_attack": re.compile('Base Wisdom Attack:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "cha_attack": re.compile('Base Charisma Attack:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
            },

            "DEFENCE": {
                "ac": re.compile('Armor Class:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-\)]+)\n'),
                "fort": re.compile('Fortitude Defense:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "ref": re.compile('Reflex Defense:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "will": re.compile('Will Defense:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
            },
            "POWERS": {
                "at-will": self.find_power(self.atwills, 6),
                "encounter": self.find_power(self.encounters, 6),
                "daily": self.find_dailys,
                "utility": self.find_utility,
            },

            "SKILLS": {
                "acrobatics": re.compile('Acrobatics:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "arcana": re.compile('Arcana:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "athletics": re.compile('Athletics:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "bluff": re.compile('Bluff:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "diplomacy": re.compile('Diplomacy:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "dungeoneering": re.compile('Dungeoneering:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "endurance": re.compile('Endurance:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "heal": re.compile('Heal:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "history": re.compile('History:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "insight": re.compile('Insight:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "intimidate": re.compile('Intimidate:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "nature": re.compile('Nature:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "perception": re.compile('Perception:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "religion": re.compile('Religion:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "stealth": re.compile('Stealth:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "streetwise": re.compile('Streetwise:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
                "thievery": re.compile('Thievery:\s+([0-9d\+\- ]+)\s*=\s*([\d \t\[\]\w\+\-]+)\n'),
            },
            "race_features": self.find_race_features,
            "class_features": self.find_class_features
        }
        self.char = {}
        f = data.split('\n')
        f = [s.strip() for s in f if s.strip()]
        self.char["character_name"] = f[0]
        self.char["gender"], self.char["race"], self.char["class"] = f[1].split()
        self.char["level"] = int(f[2].split()[1])
        self.char["alignment"] = f[3]

        for key, regex in regexes.items():
            if type(regex) is dict:
                for subkey, subregex in regex.items():
                    self.fill(self.char, subkey, subregex, data)
            else:
                self.fill(self.char, key, regex, data)
        return self.char

if __name__ == "__main__":
    data = open(os.path.join('dndgen/Characters', sys.argv[1])).read()
    conv = Converter()
    char = conv.convert(data)

    with open(os.path.join('dndgen/Characters', sys.argv[1] + '.json'), "w") as f:
        json.dump(char, f, indent=2, sort_keys=True)
