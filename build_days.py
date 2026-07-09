# -*- coding: utf-8 -*-
"""Transformace tréninkového plánu z JSON do datové struktury pro React aplikaci."""
import json

with open('/home/ubuntu/treninkovy_plan.json', encoding='utf-8') as f:
    plan = json.load(f)

# Mapování klíčů sekcí na čitelné české popisky
LABELS = {
    'rozcviceni': 'Rozcvičení',
    'hlavni_cast': 'Hlavní část',
    'core': 'Core',
    'core_doplnek': 'Core (doplněk)',
    'core_stabilizace': 'Core + stabilizace',
    'protazeni': 'Protažení',
    'vyklusani': 'Vyklusání',
    'vyklusani_a_protazeni': 'Vyklusání a protažení',
    'aktivni_pohyb': 'Aktivní pohyb',
    'mobilita_a_protazeni': 'Mobilita a protažení',
    'relaxace': 'Relaxace',
    'relaxace_a_zhodnoceni': 'Relaxace a zhodnocení',
    'technicka_cast_s_micem': 'Technická část s míčem',
    'obratnost_a_rychlost': 'Obratnost a rychlost',
    'strelba': 'Střelba',
    'varianta_1': 'Varianta 1',
    'varianta_2': 'Varianta 2',
    'doplnek': 'Doplněk',
    'hlavni_cast_tempo_beh': 'Hlavní část – tempový běh',
    'hlavni_cast_kruhovy_trenink': 'Hlavní část – kruhový trénink',
    'hlavni_cast_fartlek': 'Hlavní část – fartlek',
    'regeneracni_klus': 'Regenerační klus',
}

def label_for(key):
    return LABELS.get(key, key.replace('_', ' ').capitalize())

days = []
for d in plan['dny']:
    # Sekce popisu tréninku
    popis = []
    for key, sec in d['popis_treninku'].items():
        section = {
            'klic': key,
            'label': label_for(key),
            'nazev': sec.get('nazev', ''),
            'cas': sec.get('cas', ''),
            'popis': sec.get('popis', ''),
            'poznamka': sec.get('poznamka', ''),
            'cviky': [],
        }
        for c in sec.get('cviky', []):
            if isinstance(c, str):
                # Cvik zadaný jako prostý text – rozdělíme na název a parametry
                parts = c.split(' - ', 1)
                section['cviky'].append({
                    'nazev': parts[0].strip(),
                    'parametry': parts[1].strip() if len(parts) > 1 else '',
                    'popis': '',
                    'poznamka': '',
                })
            else:
                section['cviky'].append({
                    'nazev': c.get('nazev', ''),
                    'parametry': c.get('parametry', ''),
                    'popis': c.get('popis', c.get('technika', '')),
                    'poznamka': c.get('poznamka', c.get('odpocinok', '')),
                })
        popis.append(section)

    # Metriky
    metriky = []
    for key, m in d['metriky'].items():
        hint = m.get('poznamka') or m.get('doporuceno') or m.get('cilova_hodnota') or m.get('popis') or ''
        metriky.append({
            'klic': key,
            'nazev': m.get('nazev', ''),
            'jednotka': m.get('jednotka', ''),
            'skala': m.get('skala', ''),
            'hint': hint,
        })

    days.append({
        'id': d['den'],
        'nazev': d['nazev'],
        'zamereni': d['zamerereni'],
        'popis': popis,
        'ukoly': d['splnene_ukoly'],
        'metriky': metriky,
        'tip': d['tip_na_dnes'],
    })

out = json.dumps(days, ensure_ascii=False, indent=2)
with open('/home/ubuntu/days_data.json', 'w', encoding='utf-8') as f:
    f.write(out)
print('Vygenerováno', len(days), 'dní')
print(out[:600])
