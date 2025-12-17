import pandas as pd
import numpy as np
import ast
import os

df_units = pd.read_excel('output/16_jaren_samen.xlsx', sheet_name='Units')
df_doorstroom_pg = pd.read_excel('Brondata/Doorstroom/UHasselt_doorstroomSR_dataaanvraag2025.xlsx', sheet_name='Participatiegraad')
df_doorstroom_sr = pd.read_excel('Brondata/Doorstroom/UHasselt_doorstroomSR_dataaanvraag2025.xlsx', sheet_name='Studierendement')
df_sb = pd.read_excel('Brondata/Studiebewijzen/20251112-spending review UHasselt.xlsx', sheet_name='SB')
df_oki = pd.read_excel('Brondata/Studiebewijzen/20251112-spending review UHasselt.xlsx', sheet_name='OKI')
df_vsv = pd.read_excel('Brondata/Studiebewijzen/20251112-spending review UHasselt.xlsx', sheet_name='VSV')
df_master = pd.read_excel('output/16_jaren_samen.xlsx', sheet_name='Master')
df_master.set_index(['vestigingsplaats', 'jaar'], inplace=True)

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

def get_jaar(jaar_code):
    return f'{int(jaar_code)}-{int(jaar_code) + 1}'

def get_som_kolommen(vps, jaar, columns, df_c):
    vps = vps.replace('SO_', '')
    result = [0] * len(columns)

    for vp in vps.split('_'):
        try:
            sr = df_c.loc[(int(vp), jaar)]
            for i, col in enumerate(columns):
                result[i] += np.sum(sr[col])

        except:
            continue
    return pd.Series(result)

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
        return llngroepen['n.v.t. (okan) n.v.t. (okan)']
    try:
        return llngroepen[f'{graad}e graad {ov.lower()}']
    except:
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

def get_oki(vps, jaar, oki_df):
    lln_tot = 0
    score_tot = 0

    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            llngroepen = df_master.loc[(int(vp), jaar)]['leerlingengroepen_vp']
            llngroepen = ast.literal_eval(llngroepen)
            for key, value in llngroepen.items():
                lln_tot += value
        except:
            continue
        try:
            oki = oki_df.loc[(int(vp), jaar)]
        except:
            continue
        for graad, ov, score_oki in zip(
            oki['Graad SO inclusief modulair code'], oki['Onderwijsvorm code'], oki['gemiddelde OKI']):
                lln = get_lln_okigroep(llngroepen, graad, ov, vp, jaar)
                score_tot += lln*score_oki

    if lln_tot == 0:
        return 0
    return score_tot/lln_tot


df_units['uren-leraar_asis'] = df_units['ul_vast'] + df_units['ul_asis']
df_units['uren-leraar_tobe'] = df_units['ul_vast'] + df_units['ul_tobe']
df_units = df_units[['unit_code_so', 'jaar', 'schoolbestuur', 'net', 'llng_tobe', 'aantal_leerlingen', 
                    'uren-leraar_asis', 'directeurs_asis', 'uren-leraar_tobe',
                    'leerlingen_laatste_jaar', 'uren-leraar_laatste_jaar', 'directeurs_laatste_jaar',
                    'leerlingen_laatste_jaar_aso', 'uren-leraar_laatste_jaar_aso', 'directeurs_laatste_jaar_aso']]


# Doorstroom Participatiegraad
df_doorstroom_pg = df_doorstroom_pg[df_doorstroom_pg['Onderwijsvorm code'].isin(['ASO'])]
df_doorstroom_pg['vp_code'] = df_doorstroom_pg['Instellingscode instelling']*100 + df_doorstroom_pg['Intern volgnummer vestigingsplaats']
df_doorstroom_pg['jaar'] = df_doorstroom_pg['Schooljaar code'].apply(get_jaar)
df_doorstroom_pg.set_index(['vp_code', 'jaar'], inplace=True)
df_doorstroom_pg = df_doorstroom_pg.sort_index()
df_units[['loopbanen_HO', 'rechtstreeks_HO', 'niet_rechtstreeks_HO', 'niet_HO']] = df_units.apply(
    lambda row: get_som_kolommen(
        row['unit_code_so'], 
        row['jaar'],
        ['Aantal loopbanen HO','Aantal wel rechtstreeks doorgestroomd naar HO',
        'Aantal niet rechtstreeks doorgestroomd naar HO', 'Aantal niet doorgestroomd naar HO'],
        df_doorstroom_pg
        ), axis=1)

# Doorstroom Studierendement
df_doorstroom_sr = df_doorstroom_sr[df_doorstroom_sr['Onderwijsvorm code'].isin(['ASO'])]
df_doorstroom_sr['vp_code'] = df_doorstroom_sr['Instellingscode instelling']*100 + df_doorstroom_sr['Intern volgnummer vestigingsplaats']
df_doorstroom_sr['jaar'] = df_doorstroom_sr['Code schooljaar afstuderen SO'].apply(get_jaar)
df_doorstroom_sr.set_index(['vp_code', 'jaar'], inplace=True)
df_doorstroom_sr = df_doorstroom_sr.sort_index()
df_units[['aantal_studietrajecten', 'opgenomen_studiepunten', 'verworven_studiepunten']] = df_units.apply(
    lambda row: get_som_kolommen(
        row['unit_code_so'], 
        row['jaar'],
        ['Aantal studietrajecten','Opgenomen studiepunten als generatiestudent volgens de instelling',
        'Verworven studiepunten als generatiestudent'],
        df_doorstroom_sr
        ), axis=1)
df_units['studierendement'] = df_units['verworven_studiepunten']/df_units['opgenomen_studiepunten']

# Studiebewijzen
df_sb['vp_code'] = df_sb['Instellingscode instelling']*100 + df_sb['Intern volgnummer vestigingsplaats']
df_sb['jaar'] = df_sb['Schooljaar code'].apply(get_jaar)
df_sb.set_index(['vp_code', 'jaar'], inplace=True)
df_sb = df_sb.sort_index()
df_units[['aantal_studiebewijzen', 'aantal_diploma\'s', 'aantal_getuigschriften']] = df_units.apply(
    lambda row: get_som_kolommen(
        row['unit_code_so'], 
        row['jaar'],
        ['Aantal studiebewijzen', 'Aantal diploma\'s', 'Aantal studiegetuigschriften'],
        df_sb
    ), axis=1)

# OKI scores
df_oki['vp_code'] = df_oki['Instellingscode instelling']*100 + df_oki['Intern volgnummer vestigingsplaats']
df_oki['jaar'] = df_oki['Schooljaar code'].apply(get_jaar)
df_oki.set_index(['vp_code', 'jaar'], inplace=True)
df_oki = df_oki.sort_index()
df_units['gemiddelde_oki'] = df_units.apply(
    lambda row: get_oki(
        row['unit_code_so'], 
        row['jaar'],
        df_oki
    ), axis=1)

# Vroegtijdig Schoolverlaters
df_vsv['vp_code'] = df_vsv['Instellingscode instelling op moment VSV']*100 + df_vsv['Intern volgnummer vestigingsplaats op moment VSV']
df_vsv['jaar'] = df_vsv['Schooljaar VSV'].apply(get_jaar)
df_vsv.set_index(['vp_code', 'jaar'], inplace=True)
df_vsv = df_vsv.sort_index()
df_units[['vsv_teller', 'vsv_noemer']] = df_units.apply(
    lambda row: get_som_kolommen(
        row['unit_code_so'], 
        row['jaar'],
        ['Teller VSV', 'Noemer VSV'],
        df_vsv
    ), axis=1)
df_units['vsv_percent'] = 100*(df_units['vsv_teller']/df_units['vsv_noemer'])


df_units = df_units.rename(
    columns={
        'jaar': 'jaar_afgestudeerd_so',
        'llng_tobe': 'leerlingengroepen',
    }
)
df_units.to_excel('output/18_units_dea_master.xlsx', index=False)