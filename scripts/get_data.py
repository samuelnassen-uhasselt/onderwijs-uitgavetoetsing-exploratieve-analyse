import pandas as pd
import pickle
import os
import ast
import numpy as np


def get_jaar(jaar_code):
    return f'{int(jaar_code)}-{int(jaar_code) + 1}'

df_master_vp = pd.read_excel('output/16_jaren_samen.xlsx', sheet_name='Master')
df_master_vp.set_index(['vestigingsplaats', 'jaar'], inplace=True)
df_extra_vp = pd.read_excel('output/16_jaren_samen.xlsx', sheet_name='Extra Omkadering')
df_extra_vp.set_index(['vestigingsplaats', 'jaar'], inplace=True)

df_oki_17_23 = pd.read_excel('Brondata\\Studiebewijzen\\20251112-spending review UHasselt.xlsx', sheet_name='OKI')
df_oki_17_23['vp_code'] = df_oki_17_23['Instellingscode instelling']*100 + df_oki_17_23['Intern volgnummer vestigingsplaats']
df_oki_17_23['jaar'] = df_oki_17_23['Schooljaar code'].apply(get_jaar)
df_oki_17_23['Aantal inschrijvingen'] = 'missend 17-23'

df_oki_24 = pd.read_excel('Brondata\\OKI\\SO311_VPL_2425.xlsx')
df_oki_24['vp_code'] = df_oki_24['Instellingscode']*100 + df_oki_24['Intern volgnummer vestigingsplaats']
df_oki_24['gemiddelde OKI'] = df_oki_24['Onderwijs Kansarmoede Indicator (OKI)']/df_oki_24['Aantal inschrijvingen']
df_oki_24[['Graad SO inclusief modulair code', 'Onderwijsvorm code']] = pd.Series(['missend 24', 'missend 24'])
df_oki_24 = df_oki_24.rename(
    columns={
        'Huidig schooljaar': 'jaar',
        'Instellingscode': 'Instellingscode instelling', 
    }
)
df_oki_24 = df_oki_24[['Schooljaar code', 'Instellingscode instelling', 'Intern volgnummer vestigingsplaats',
                       'Graad SO inclusief modulair code', 'Onderwijsvorm code', 'gemiddelde OKI', 'vp_code', 'jaar', 'Aantal inschrijvingen']]

df_oki = pd.concat([df_oki_17_23, df_oki_24], ignore_index=True)
df_oki_laatste = df_oki[df_oki['Graad SO inclusief modulair code'] == 3]
df_oki.set_index(['vp_code', 'jaar'], inplace=True)
df_oki = df_oki.sort_index()
df_oki_laatste.set_index(['vp_code', 'jaar'], inplace=True)
df_oki_laatste = df_oki_laatste.sort_index()

def load_modulair_dfs():
    modulair_dfs = {}
    folder = 'output/jaren'
    jaren_folders = [f for f in os.listdir(folder)]
    for jaar in jaren_folders:
        inschrijvingen = pd.read_excel(f'Brondata/Inschrijvingen/inschrijvingen-leerplicht-instellingen-dataset-{jaar}-1feb.xlsx')
        inschrijvingen = inschrijvingen[
            (inschrijvingen['onderwijsvorm'] == 'bso') &
            (inschrijvingen['graad_so_code'] == 'n.v.t. (modulair)')
        ]
        modulair_dfs[jaar] = inschrijvingen
    
    with open('output\\modulair_dfs_dict.pkl', 'wb') as f:
        pickle.dump(modulair_dfs, f)

def get_lln_okigroep(llngroepen, graad, ov, vp, jaar):
    aantal = 0
    if graad == '1':
        for llngr in llngroepen.keys():
            if '1e graad' in llngr:
                aantal += llngroepen[llngr]
        return aantal
    if graad == 'H':
        return llngroepen['hbo']
    if graad == 'OKAN':
        return llngroepen['okan']
    try:
        return llngroepen[f'{graad}e graad {ov.lower()}']
    except:
        if 'modulair_dfs_dict.pkl' not in os.listdir('output'):
            load_modulair_dfs()
        with open('output\\modulair_dfs_dict.pkl', 'rb') as f:
            modulair_dfs = pickle.load(f)
        inschrijvingen = modulair_dfs[jaar]
        inschrijvingen = inschrijvingen[
            (inschrijvingen['instellingsnummer'] == int(vp[:-2])) &
            (inschrijvingen['intern_volgnr_vpl'] == int(vp[-2:]))
        ]
        aantal  = 0
        for groep, inschr in zip(
            inschrijvingen['administratieve_groep'], inschrijvingen['aantal_inschrijvingen']):
            if '{graad}e gr' in groep:
                aantal += inschr
        return aantal

def get_oki(vps, jaar, laatste):
    lln_tot = 0
    score_tot = 0

    if pd.notna(vps):
        vps = vps.replace('SO_', '')
    else:
        return
    for vp in vps.split('_'):
        if jaar == '2024-2025':
            try:
                oki = df_oki.loc[(int(vp), jaar)]
                inschr = df_master_vp.loc[(int(vp), jaar)]['aantal_inschrijvingen_vp']
                if pd.notna(inschr):
                    lln_tot += inschr
                    score_tot += inschr * oki['gemiddelde OKI'].sum()
            except:
                continue
            continue
        try:
            llngroepen = df_master_vp.loc[(int(vp), jaar)]['leerlingengroepen_vp']
            llngroepen = ast.literal_eval(llngroepen)
            for key, value in llngroepen.items():
                lln_tot += value
        except:
            continue
        try:
            if laatste:
                oki = df_oki_laatste.loc[(int(vp), jaar)]
            else:
                oki = df_oki.loc[(int(vp), jaar)]
        except:
            continue
        for graad, ov, score_oki in zip(
            oki['Graad SO inclusief modulair code'], oki['Onderwijsvorm code'], oki['gemiddelde OKI']):
                lln = get_lln_okigroep(llngroepen, graad, ov, vp, jaar)
                score_tot += lln*score_oki

    if lln_tot == 0:
        return 0
    return score_tot/lln_tot

def get_som_kolommen(vps, jaar, columns, df_c):
    if pd.notna(vps):
        vps = vps.replace('SO_', '')
    else:
        return
    result = [0] * len(columns)

    for vp in vps.split('_'):
        try:
            sr = df_c.loc[(int(vp), jaar)]
            for i, col in enumerate(columns):
                result[i] += np.sum(sr[col])

        except:
            continue
    return pd.Series(result)

def get_aantal_instellingsnummers(vps):
    vps = vps.replace('SO_', '')
    inst = list(set([v[:-2] for v in vps.split('_')]))
    return len(inst)


omk_naar_euro = {
    'ul': 69073 / 21.23,
    'dir': 120 * 752.4,
    'punten': 752.4,
    'adj_dir': 97010,
    'ta_org': 0,
    'tac_bonus': 0,
    'tac_org': 0,
    'teelt': 0,
    'topsport': 0
}


def get_dea_input(vps, jaar):
    if pd.notna(vps):
        vps = vps.replace('SO_', '')
    else:
        return
    
    asis= 0
    asis_laatste = 0
    tobe = 0
    tobe_laatste = 0
    herverdeeld = 0
    herverdeeld_laatste = 0

    for vp in vps.split('_'):
        try:
            master = df_master_vp.loc[(int(vp), jaar)].fillna(0)
            extra = df_extra_vp.loc[(int(vp), jaar)].fillna(0)
        except KeyError:
            continue
        forfaitair = extra['forfaitair_pakket']
        min_pakket = extra['minimumpakket']

        if not pd.notna(forfaitair) and forfaitair > 0:
            ul_asis = forfaitair
            ul_asis_laatste = extra['forfaitair_pakket_laatste']
        elif not pd.notna(min_pakket) and min_pakket > 0:
            ul_asis = min_pakket
            ul_asis_laatste = extra['minimumpakket_laatste']
        else:
            ul_asis = (master['vaste_ul_vp'] + master['ul_vp']) * 0.9657 + extra['extra_ul_aanwendbaar']
            ul_asis_laatste = ((master['ul_vast_vp_laatste_jaar'] + master['ul_deg_asis_vp_laatste_jaar']) * 0.9657 + 
                               extra['extra_ul_aanwendbaar_laatste'])
        ul_tobe = (master['vaste_ul_vp'] + master['ul_tobe']) * 0.9657 + extra['extra_ul_aanwendbaar']
        ul_tobe_laatste = ((master['ul_vast_vp_laatste_jaar'] + master['ul_laatste_jaar_tobe']) * 0.9657 + 
                               extra['extra_ul_aanwendbaar_laatste'])
        ul_herverdeeld = (master['vaste_ul_vp'] + master['ul_herverdeeld']) * 0.9657 + extra['extra_ul_aanwendbaar']
        ul_herverdeeld_laatste = ((master['ul_vast_vp_laatste_jaar'] + master['ul_laatste_herverdeeld']) * 0.9657 + 
                               extra['extra_ul_aanwendbaar_laatste'])

        dir_asis = master['directeur_vp']
        dir_asis_laatste = master['dir_laatste_jaar']
        dir_tobe = master['directeurs_tobe']
        dir_tobe_laatste = master['directeurs_laatste_jaar_tobe']
        punten_dir_herverdeeld = master['punten_dir_herverdeeld']
        punten_dir_herverdeeld_laatste = master['punten_dir_laatste_herverdeeld']

        werkingsmiddelen = extra['werkingsmiddelen_vp']
        werkingsmiddelen_laatste = extra['werkingsmiddelen_vp_laatste']

        punten = extra['extra_punten_aanwendbaar']
        punten_laatste = extra['extra_punten_aanwendbaar_laatste']

        adj_dir, ta_org, tac_bonus, tac_org, teelt, topsport = extra[[
            'Adjunct-directeur', 'TA organiek', 'TAC bonusambt', 'TAC organiek',
            'Teeltleider', 'Topsportschoolcoördinator'
        ]]
        adj_dir_laatste, ta_org_laatste, tac_bonus_laatste, tac_org_laatste, teelt_laatste, topsport_laatste = extra[[
            'Adjunct-directeur_laatste', 'TA organiek_laatste', 'TAC bonusambt_laatste', 'TAC organiek_laatste',
            'Teeltleider_laatste', 'Topsportschoolcoördinator_laatste'
        ]]

        euro_extra = (werkingsmiddelen + punten*omk_naar_euro['punten'] + adj_dir*omk_naar_euro['adj_dir'] + 
                      ta_org*omk_naar_euro['ta_org'] + tac_bonus*omk_naar_euro['tac_bonus'] + 
                      tac_org*omk_naar_euro['tac_org'] + teelt*omk_naar_euro['teelt'] + topsport*omk_naar_euro['topsport'])
        euro_extra_laatste = (werkingsmiddelen_laatste + punten_laatste*omk_naar_euro['punten'] + 
                              adj_dir_laatste*omk_naar_euro['adj_dir'] + ta_org_laatste*omk_naar_euro['ta_org'] + 
                              tac_bonus_laatste*omk_naar_euro['tac_bonus'] + tac_org_laatste*omk_naar_euro['tac_org'] + 
                              teelt_laatste*omk_naar_euro['teelt'] + topsport_laatste*omk_naar_euro['topsport'])
        
        asis += euro_extra + ul_asis*omk_naar_euro['ul'] + dir_asis*omk_naar_euro['dir']
        asis_laatste += euro_extra_laatste + ul_asis_laatste*omk_naar_euro['ul'] + dir_asis_laatste*omk_naar_euro['dir']
        tobe += euro_extra + ul_tobe*omk_naar_euro['ul'] + dir_tobe*omk_naar_euro['dir']
        tobe_laatste += euro_extra_laatste + ul_tobe_laatste*omk_naar_euro['ul'] + dir_tobe_laatste*omk_naar_euro['dir']

        herverdeeld += euro_extra + ul_herverdeeld*omk_naar_euro['ul'] + punten_dir_herverdeeld*omk_naar_euro['punten']
        herverdeeld_laatste += (euro_extra_laatste + ul_herverdeeld_laatste*omk_naar_euro['ul'] + 
                                punten_dir_herverdeeld_laatste*omk_naar_euro['punten'])

    return pd.Series([asis, asis_laatste, tobe, tobe_laatste, herverdeeld, herverdeeld_laatste])