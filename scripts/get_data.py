import pandas as pd
import pickle
import os
import ast
import numpy as np


def get_jaar(jaar_code):
    return f'{int(jaar_code)}-{int(jaar_code) + 1}'

df_master_vp = pd.read_excel('output/16_jaren_samen.xlsx', sheet_name='Master')
df_master_vp.set_index(['vestigingsplaats', 'jaar'], inplace=True)

df_oki = pd.read_excel('Brondata/Studiebewijzen/20251112-spending review UHasselt.xlsx', sheet_name='OKI')
df_oki['vp_code'] = df_oki['Instellingscode instelling']*100 + df_oki['Intern volgnummer vestigingsplaats']
df_oki['jaar'] = df_oki['Schooljaar code'].apply(get_jaar)
df_oki.set_index(['vp_code', 'jaar'], inplace=True)
df_oki = df_oki.sort_index()

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

def get_oki(vps, jaar):
    lln_tot = 0
    score_tot = 0

    if pd.notna(vps):
        vps = vps.replace('SO_', '')
    else:
        return
    for vp in vps.split('_'):
        try:
            llngroepen = df_master_vp.loc[(int(vp), jaar)]['leerlingengroepen_vp']
            llngroepen = ast.literal_eval(llngroepen)
            for key, value in llngroepen.items():
                lln_tot += value
        except:
            continue
        try:
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
