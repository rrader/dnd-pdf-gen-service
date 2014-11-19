import json
import os
from fdfgen import forge_fdf
import sys

if __name__ == "__main__":
    data = json.load(open(os.path.join("Characters", sys.argv[1]+'.json')))
    level2 = int(data.get('level'))//2
    info = dict([
            ('str_mod', data.get('str', '')[1]),
            ('con_mod', data.get('con', '')[1]),
            ('dex_mod', data.get('dex', '')[1]),
            ('int_mod', data.get('int', '')[1]),
            ('wis_mod', data.get('wis', '')[1]),
            ('cha_mod', data.get('cha', '')[1])
            ])
    fields = [
            ('class', data.get('class', '')),
            ('race', data.get('race', '')),
            ('size', data.get('size', '')),
            ('age', data.get('age', '')),
            ('gender', data.get('gender', '')),
            ('height', data.get('height', '')),
            ('weight', data.get('weight', '')),
            ('deity', data.get('deity', '')),
            ('alignment', data.get('alignment', '')),
            ('affiliations', data.get('affiliations', '')),
            ('player_name', data.get('player_name', '')),
            ('level', data.get('level', '')),
            ('initiative_misc', data.get('initiative_misc', '')),
            ('initiative_dex', data.get('dex', '')[1]),
            ('initiative_score', data.get('initiative_score', '')[0]),
            ('con', data.get('con', '')[0]),
            ('dex', data.get('dex', '')[0]),
            ('int', data.get('int', '')[0]),
            ('wis', data.get('wis', '')[0]),
            ('str_mod_level', int(data.get('str', '')[1]) + level2),
            ('con_mod_level', int(data.get('con', '')[1]) + level2),
            ('dex_mod_level', int(data.get('dex', '')[1]) + level2),
            ('int_mod_level', int(data.get('int', '')[1]) + level2),
            ('wis_mod_level', int(data.get('wis', '')[1]) + level2),
            ('cha_mod_level', int(data.get('cha', '')[1]) + level2),
            ('initiative_level', level2),
            ('ref_level', data.get('ref_level', '')),
            ('ref_ability', data.get('ref_ability', '')),
            ('ref_class', data.get('ref_class', '')),
            ('ref_feat', data.get('ref_feat', '')),
            ('ref_enh', data.get('ref_enh', '')),
            ('ref_misc1', data.get('ref_misc1', '')),
            ('ref_misc2', data.get('ref_misc2', '')),
            ('fort_level', data.get('fort_level', '')),
            ('fort_ability', data.get('fort_ability', '')),
            ('fort_class', data.get('fort_class', '')),
            ('fort_feat', data.get('fort_feat', '')),
            ('fort_enh', data.get('fort_enh', '')),
            ('fort_misc1', data.get('fort_misc1', '')),
            ('fort_misc2', data.get('fort_misc2', '')),
            ('ac_armor', data.get('ac_armor', '')),
            ('ac_class', data.get('ac_class', '')),
            ('ac_feat', data.get('ac_feat', '')),
            ('ac_enh', data.get('ac_enh', '')),
            ('ac_misc1', data.get('ac_misc1', '')),
            ('ac_misc2', data.get('ac_misc2', '')),
            ('ac_level', data.get('ac_level', '')),
            ('ac', data.get('ac', '')[0]),
            ('fort', data.get('fort', '')[0]),
            ('ref', data.get('ref', '')[0]),
            ('str', data.get('str', '')[0]),
            ('speed_item', data.get('speed_item', '')),
            ('speed_misc', data.get('speed_misc', '')),
            ('speed_armor', data.get('speed_armor', '')),
            ('speed_base', data.get('speed_base', '')),
            ('initiative_conditions', data.get('initiative_conditions', '')),
            ('ref_conditions', data.get('ref_conditions', '')),
            ('fort_conditions', data.get('fort_conditions', '')),
            ('speed', data.get('speed', '')),
            ('pass_insight', int(data.get('insight', '')[0]) + 10),
            ('pass_perception', int(data.get('insight', '')[0]) + 10),
            ('pass_insight_skill', data.get('insight', '')[0]),
            ('pass_perception_skill', data.get('insight', '')[0]),
            ('ac_conditions', data.get('ac_conditions', '')),
            ('speed_special', data.get('speed_special', '')),
            ('acrobatics', data.get('acrobatics', '')[0]),
            ('acrobatics_mod', int(info['dex_mod']) + level2),
            ('acrobatics_trnd', data.get('acrobatics_trnd', '')),
            ('acrobatics_pen', data.get('acrobatics_pen', '')),
            ('acrobatics_misc', data.get('acrobatics_misc', '')),
            ('arcana', data.get('arcana', '')[0]),
            ('arcana_mod', int(info['int_mod']) + level2),
            ('arcana_trnd', data.get('arcana_trnd', '')),
            ('arcana_misc', data.get('arcana_misc', '')),
            ('athletics', data.get('athletics', '')[0]),
            ('athletics_mod', int(info['str_mod']) + level2),
            ('athletics_trnd', data.get('athletics_trnd', '')),
            ('athletics_pen', data.get('athletics_pen', '')),
            ('athletics_misc', data.get('athletics_misc', '')),
            ('bluff', data.get('bluff', '')[0]),
            ('bluff_mod', int(info['cha_mod']) + level2),
            ('bluff_trnd', data.get('bluff_trnd', '')),
            ('bluff_misc', data.get('bluff_misc', '')),
            ('diplomacy', data.get('diplomacy', '')[0]),
            ('diplomacy_mod', int(info['cha_mod']) + level2),
            ('diplomacy_trnd', data.get('diplomacy_trnd', '')),
            ('diplomacy_misc', data.get('diplomacy_misc', '')),
            ('dungeoneering', data.get('dungeoneering', '')[0]),
            ('dungeoneering_trnd', data.get('dungeoneering_trnd', '')),
            ('dungeoneering_misc', data.get('dungeoneering_misc', '')),
            ('dungeoneering_mod', int(info['wis_mod']) + level2),
            ('endurance', data.get('endurance', '')[0]),
            ('endurance_mod', int(info['con_mod']) + level2),
            ('endurance_trnd', data.get('endurance_trnd', '')),
            ('endurance_pen', data.get('endurance_pen', '')),
            ('endurance_misc', data.get('endurance_misc', '')),
            ('heal', data.get('heal', '')[0]),
            ('heal_mod', int(info['wis_mod']) + level2),
            ('heal_trnd', data.get('heal_trnd', '')),
            ('heal_misc', data.get('heal_misc', '')),
            ('history', data.get('history', '')[0]),
            ('history_mod', int(info['int_mod']) + level2),
            ('history_trnd', data.get('history_trnd', '')),
            ('history_misc', data.get('history_misc', '')),
            ('insight', data.get('insight', '')[0]),
            ('insight_mod', int(info['wis_mod']) + level2),
            ('insight_trnd', data.get('insight_trnd', '')),
            ('insight_misc', data.get('insight_misc', '')),
            ('intimidate', data.get('intimidate', '')[0]),
            ('intimidate_mod', int(info['cha_mod']) + level2),
            ('intimidate_trnd', data.get('intimidate_trnd', '')),
            ('intimidate_misc', data.get('intimidate_misc', '')),
            ('nature', data.get('nature', '')[0]),
            ('nature_mod', int(info['wis_mod']) + level2),
            ('nature_trnd', data.get('nature_trnd', '')),
            ('nature_misc', data.get('nature_misc', '')),
            ('perception', data.get('perception', '')[0]),
            ('perception_mod', int(info['wis_mod']) + level2),
            ('perception_trnd', data.get('perception_trnd', '')),
            ('perception_misc', data.get('perception_misc', '')),
            ('religion', data.get('religion', '')[0]),
            ('religion_mod', int(info['int_mod']) + level2),
            ('religion_trnd', data.get('religion_trnd', '')),
            ('religion_misc', data.get('religion_misc', '')),
            ('stealth', data.get('stealth', '')[0]),
            ('stealth_mod', int(info['dex_mod']) + level2),
            ('stealth_trnd', data.get('stealth_trnd', '')),
            ('stealth_pen', data.get('stealth_pen', '')),
            ('stealth_misc', data.get('stealth_misc', '')),
            ('streetwise', data.get('streetwise', '')[0]),
            ('streetwise_mod', int(info['cha_mod']) + level2),
            ('streetwise_trnd', data.get('streetwise_trnd', '')),
            ('streetwise_misc', data.get('streetwise_misc', '')),
            ('thievery', data.get('thievery', '')[0]),
            ('thievery_mod', int(info['dex_mod']) + level2),
            ('thievery_trnd', data.get('thievery_trnd', '')),
            ('thievery_pen', data.get('thievery_pen', '')),
            ('thievery_misc', data.get('thievery_misc', '')),
            ('senses_special', data.get('senses_special', '')),
            ('will_level', data.get('will_level', '')),
            ('will_ability', data.get('will_ability', '')),
            ('will', data.get('will', '')[0]),
            ('attack_workspace_level', data.get('attack_workspace_level', '')),
            ('attack_workspace_ability', data.get('attack_workspace_ability', '')),
            ('attack_workspace_class', data.get('attack_workspace_class', '')),
            ('attack_workspace_prof', data.get('attack_workspace_prof', '')),
            ('attack_workspace_feat', data.get('attack_workspace_feat', '')),
            ('attack_workspace_enh', data.get('attack_workspace_enh', '')),
            ('attack_workspace_misc', data.get('attack_workspace_misc', '')),
            ('attack_workspace_level2', data.get('attack_workspace_level2', '')),
            ('attack_workspace_ability2', data.get('attack_workspace_ability2', '')),
            ('attack_workspace_prof2', data.get('attack_workspace_prof2', '')),
            ('attack_workspace_feat2', data.get('attack_workspace_feat2', '')),
            ('attack_workspace_enh2', data.get('attack_workspace_enh2', '')),
            ('attack_workspace_misc2', data.get('attack_workspace_misc2', '')),
            ('attack_workspace_bonus', data.get('attack_workspace_bonus', '')),
            ('attack_workspace_bonus2', data.get('attack_workspace_bonus2', '')),
            ('max_hp', data.get('max_hp', '')),
            ('attack_workspace_class2', data.get('attack_workspace_class2', '')),
            ('surge_value', data.get('surge_value', '')),
            ('bloodied', data.get('bloodied', '')),
            ('attack_workspace2', data.get('attack_workspace2', '')),
            ('save_throw_mods', data.get('save_throw_mods', '')),
            ('resistances', data.get('resistances', '')),
            ('current_conditions', data.get('current_conditions', '')),
            ('surger_day', data.get('surger_day', '')),
            ('action_points', 1),
            ('will_conditions', data.get('will_conditions', '')),
            ('character_name', data.get('character_name', '')),
            ('race_ability_mods', data.get('race_ability_mods', '')),
            ('class1', data.get('class_features', '')[1-1]),
            ('class2', data.get('class_features', '')[2-1]),
            ('class3', data.get('class_features', '')[3-1]),
            ('class4', data.get('class_features', '')[4-1]),
            ('class5', data.get('class_features', '')[5-1]),
            ('class6', data.get('class_features', '')[6-1]),
            ('class7', data.get('class_features', '')[7-1]),
            ('class8', data.get('class_features', '')[8-1]),
            ('class9', data.get('class_features', '')[9-1]),
            ('class10', data.get('class_features', '')[10-1]),
            ('class11', data.get('class_features', '')[11-1]),
            ('class12', data.get('class_features', '')[12-1]),
            ('class13', data.get('class_features', '')[13-1]),
            ('class14', data.get('class_features', '')[14-1]),
            ('lang1', data.get('Languages', '')[1-1]),
            ('lang2', data.get('Languages', '')[2-1]),
            ('lang3', data.get('Languages', '')[3-1]),
            ('feat1', data.get('Feats', '')[1-1]),
            ('feat2', data.get('Feats', '')[2-1]),
            ('feat3', data.get('Feats', '')[3-1]),
            ('feat4', data.get('Feats', '')[4-1]),
            ('feat5', data.get('Feats', '')[5-1]),
            ('feat6', data.get('Feats', '')[6-1]),
            ('feat7', data.get('Feats', '')[7-1]),
            ('feat8', data.get('Feats', '')[8-1]),
            ('feat9', data.get('Feats', '')[9-1]),
            ('feat10', data.get('Feats', '')[10-1]),
            ('feat11', data.get('Feats', '')[11-1]),
            ('feat12', data.get('Feats', '')[12-1]),
            ('feat13', data.get('Feats', '')[13-1]),
            ('feat14', data.get('Feats', '')[14-1]),
            ('feat15', data.get('Feats', '')[15-1]),
            ('feat16', data.get('Feats', '')[16-1]),
            ('attack_workspace', data.get('attack_workspace', '')),
            ('damage_workspace2', data.get('damage_workspace2', '')),
            ('will_class', data.get('will_class', '')),
            ('will_feat', data.get('will_feat', '')),
            ('will_enh', data.get('will_enh', '')),
            ('will_misc1', data.get('will_misc1', '')),
            ('will_misc2', data.get('will_misc2', '')),
            ('damage_workspace_ability', data.get('damage_workspace_ability', '')),
            ('damage_workspace_misc2', data.get('damage_workspace_misc2', '')),
            ('damage_workspace_feat', data.get('damage_workspace_feat', '')),
            ('damage_workspace_enh', data.get('damage_workspace_enh', '')),
            ('damage_workspace_misc1', data.get('damage_workspace_misc1', '')),
            ('damage_workspace_feat2', data.get('damage_workspace_feat2', '')),
            ('damage_workspace_enh2', data.get('damage_workspace_enh2', '')),
            ('damage_workspace_misc12', data.get('damage_workspace_misc12', '')),
            ('damage_workspace_misc22', data.get('damage_workspace_misc22', '')),
            ('damage_workspace_ability2', data.get('damage_workspace_ability2', '')),
            ('damage_workspace_damage2', data.get('damage_workspace_damage2', '')),
            ('action_points_additional', data.get('action_points_additional', '')),
            ('cha', data.get('cha', '')[0]),

            ('basic_weapon1', data.get('Attacks', '')[0][0]),
            ('basic_attack1', data.get('Attacks', '')[0][1]),
            ('basic_defense1', data.get('Attacks', '')[0][2]),
            ('basic_damage1', data.get('Attacks', '')[0][3]),

            ('basic_weapon2', data.get('Attacks', '')[1][0]),
            ('basic_attack2', data.get('Attacks', '')[1][1]),
            ('basic_defense2', data.get('Attacks', '')[1][2]),
            ('basic_damage2', data.get('Attacks', '')[1][3]),

            ('basic_weapon3', data.get('Attacks', '')[2][0]),
            ('basic_attack3', data.get('Attacks', '')[2][1]),
            ('basic_defense3', data.get('Attacks', '')[2][2]),
            ('basic_damage3', data.get('Attacks', '')[2][3]),
            
            ('basic_weapon4', data.get('Attacks', '')[3][0]),
            ('basic_attack4', data.get('Attacks', '')[3][1]),
            ('basic_defense4', data.get('Attacks', '')[3][2]),
            ('basic_damage4', data.get('Attacks', '')[3][3]),
            
            ('damage_workspace_damage', data.get('damage_workspace_damage', '')),
            ('damage_workspace', data.get('damage_workspace', '')),
            
            ('race1', data.get('race_features', '')[0]),
            ('race2', data.get('race_features', '')[1]),
            ('race3', data.get('race_features', '')[2]),
            ('race4', data.get('race_features', '')[3]),
            ('race5', data.get('race_features', '')[4]),
            ('race6', data.get('race_features', '')[5]),
            ('race7', data.get('race_features', '')[6]),
            ('race8', data.get('race_features', '')[7]),
            ('feat17', data.get('feat17', '')),
            ('atwill1', data.get('at-will', '')[1-1]),
            ('atwill2', data.get('at-will', '')[2-1]),
            ('atwill3', data.get('at-will', '')[3-1]),
            ('atwill4', data.get('at-will', '')[4-1]),
            ('atwill5', data.get('at-will', '')[5-1]),
            ('atwill6', data.get('at-will', '')[6-1]),
            ('encounter1', data.get('encounter', '')[1-1]),
            ('encounter2', data.get('encounter', '')[2-1]),
            ('encounter3', data.get('encounter', '')[3-1]),
            ('encounter4', data.get('encounter', '')[4-1]),
            ('encounter5', data.get('encounter', '')[5-1]),
            ('encounter6', data.get('encounter', '')[6-1]),
            ('daily1', data.get('daily', '')[1-1]),
            ('daily2', data.get('daily', '')[2-1]),
            ('daily3', data.get('daily', '')[3-1]),
            ('daily4', data.get('daily', '')[4-1]),
            ('daily5', data.get('daily', '')[5-1]),
            ('daily6', data.get('daily', '')[6-1]),
            ('utility1', data.get('utility', '')[1-1][0]),
            ('utility2', data.get('utility', '')[2-1][0]),
            ('utility3', data.get('utility', '')[3-1][0]),
            ('utility4', data.get('utility', '')[4-1][0]),
            ('utility5', data.get('utility', '')[5-1][0]),
            ('utility6', data.get('utility', '')[6-1][0]),
            ('utility7', data.get('utility', '')[7-1][0]),
            ('utility8', data.get('utility', '')[8-1][0]),
            ('magic1', data.get('magic1', '')),
            ('magic2', data.get('magic2', '')),
            ('magic3', data.get('magic3', '')),
            ('magic4', data.get('magic4', '')),
            ('magic5', data.get('magic5', '')),
            ('magic6', data.get('magic6', '')),
            ('magic7', data.get('magic7', '')),
            ('magic8', data.get('magic8', '')),
            ('magic9', data.get('magic9', '')),
            ('magic10', data.get('magic10', '')),
            ('magic11', data.get('magic11', '')),
            ('magic12', data.get('magic12', '')),
            ('magic13', data.get('magic13', '')),
            ('magic14', data.get('magic14', '')),
            ('magic15', data.get('magic15', '')),
            ('magic16', data.get('magic16', '')),
            ('magic17', data.get('magic17', '')),
            ('magic18', data.get('magic18', '')),
            ('magic19', data.get('magic19', '')),
            ('magic20', data.get('magic20', '')),
            ('magic21', data.get('magic21', '')),
            ('magic22', data.get('magic22', '')),
            ('magic23', data.get('magic23', '')),
            ('magic24', data.get('magic24', '')),
            ('magic25', data.get('magic25', '')),
            ('personality1', data.get('personality1', '')),
            ('personality2', data.get('personality2', '')),
            ('personality3', data.get('personality3', '')),
            ('personality4', data.get('personality4', '')),
            ('personality5', data.get('personality5', '')),
            ('personality6', data.get('personality6', '')),
            ('mannerisms1', data.get('mannerisms1', '')),
            ('mannerisms2', data.get('mannerisms2', '')),
            ('mannerisms3', data.get('mannerisms3', '')),
            ('mannerisms4', data.get('mannerisms4', '')),
            ('mannerisms5', data.get('mannerisms5', '')),
            ('background1', data.get('background1', '')),
            ('background2', data.get('background2', '')),
            ('background3', data.get('background3', '')),
            ('background4', data.get('background4', '')),
            ('equipment2', data.get('equipment2', '')),
            ('equipment3', data.get('equipment3', '')),
            ('equipment4', data.get('equipment4', '')),
            ('equipment5', data.get('equipment5', '')),
            ('equipment6', data.get('equipment6', '')),
            ('equipment7', data.get('equipment7', '')),
            ('equipment8', data.get('equipment8', '')),
            ('equipment9', data.get('equipment9', '')),
            ('equipment10', data.get('equipment10', '')),
            ('equipment1', data.get('equipment1', '')),
            ('rituals1', "%s %s" % tuple(data.get('Rituals', '')[1-1])),
            ('rituals2', "%s %s" % tuple(data.get('Rituals', '')[2-1])),
            ('rituals3', "%s %s" % tuple(data.get('Rituals', '')[3-1])),
            ('rituals4', "%s %s" % tuple(data.get('Rituals', '')[4-1])),
            ('rituals5', "%s %s" % tuple(data.get('Rituals', '')[5-1])),
            ('rituals6', "%s %s" % tuple(data.get('Rituals', '')[6-1])),
            ('rituals7', "%s %s" % tuple(data.get('Rituals', '')[7-1])),
            ('rituals8', "%s %s" % tuple(data.get('Rituals', '')[8-1])),
            ('rituals9', "%s %s" % tuple(data.get('Rituals', '')[9-1])),
            ('rituals10', "%s %s" % tuple(data.get('Rituals', '')[10-1])),
            ('session1', data.get('session1', '')),
            ('session2', data.get('session2', '')),
            ('session3', data.get('session3', '')),
            ('session4', data.get('session4', '')),
            ('session5', data.get('session5', '')),
            ('session6', data.get('session6', '')),
            ('session7', data.get('session7', '')),
            ('session8', data.get('session8', '')),
            ('session9', data.get('session9', '')),
            ('session10', data.get('session10', '')),
            ('session11', data.get('session11', '')),
            ('session12', data.get('session12', '')),
            ('companion2', data.get('companion2', '')),
            ('companion3', data.get('companion3', '')),
            ('companion4', data.get('companion4', '')),
            ('companion5', data.get('companion5', '')),
            ('companion6', data.get('companion6', '')),
            ('companion7', data.get('companion7', '')),
            ('companion8', data.get('companion8', '')),
            ('companion1', data.get('companion1', '')),
            ('notes2', data.get('notes2', '')),
            ('notes3', data.get('notes3', '')),
            ('notes4', data.get('notes4', '')),
            ('notes5', data.get('notes5', '')),
            ('notes6', data.get('notes6', '')),
            ('notes7', data.get('notes7', '')),
            ('notes8', data.get('notes8', '')),
            ('notes1', data.get('notes1', '')),
            ('wealth1', data.get('wealth1', '')),
            ('wealth2', data.get('wealth2', '')),
            ('wealth3', data.get('wealth3', '')),
            ('wealth4', data.get('wealth4', '')),
            ]
    fields += list(info.items())
    fdf = forge_fdf("", fields, [], [], [])
    fdf_file = open("data.fdf", "wb")
    fdf_file.write(fdf)
    fdf_file.close()