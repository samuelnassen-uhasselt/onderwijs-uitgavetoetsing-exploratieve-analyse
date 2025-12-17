import ast
import numpy as np
import pandas as pd
import degressieve_ul_llngroepen as dul
import sys

df_units = pd.read_excel('Brondata\\Units en complexen\\SO_complexen_DLinfo.xlsx')
df_vestigingen = pd.read_excel(f'output/jaren/{sys.argv[1]}/5_master_ul_dir.xlsx').set_index('vestigingsplaats')

def get_bestuur(vps):
    result = []
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            bestuur = df_vestigingen.loc[int(vp), 'schoolbestuur']
            result.append(bestuur)
        except:
            result.append(np.nan)
    result = [i for i in result if pd.notna(i)]
    result = list(set(result))
    if len(result) == 1:
        return result[0]
    return result

def get_net(vps):
    result = []
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            net = df_vestigingen.loc[int(vp), 'net']
            result.append(net)
        except:
            result.append(np.nan)
    result = [i for i in result if pd.notna(i)]
    result = list(set(result))
    if len(result) == 1:
        return result[0]
    return result

def get_llngroepen_for_vestingsplaatsen(vps):
    result = {}
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            llngroep = df_vestigingen.loc[int(vp), 'ul_llngroepen']
            if pd.notna(llngroep):
                llngroep = ast.literal_eval(llngroep)
            result[vp] = (llngroep)
        except:
            result[vp] = np.nan

    return result

def get_llngroepen_tobe(llngroepen_asis):
    result = {}
    for vp, llng in llngroepen_asis.items():
        if pd.notna(llng):
            for key, value in llng.items():
                if key not in result:
                    result[key] = {'inschrijvingen': 0}
                result[key]['inschrijvingen'] += value['inschrijvingen']

    for key, value in result.items():
        result[key]['uren-leraar'] = dul.get_degressieve_uren_leraar(key, value['inschrijvingen'])
    return result

def get_llngroepen_set(llngroepen):
    result = set()
    for key, value in llngroepen.items():
        if pd.notna(value):
            result.update(value.keys())
    return sorted(list(result))

def get_aantal_leerlingen(llngroepen):
    result = 0
    for key, value in llngroepen.items():
        result += value['inschrijvingen']
    return result

def get_llngroep_vul(vps):
    result = {}
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            llngroep = df_vestigingen.loc[int(vp), 'leerlingengroepen_vaste_ul']
            if pd.notna(llngroep):
                llngroep = ast.literal_eval(llngroep)
            result[vp] = (llngroep)
        except:
            result[vp] = np.nan

    return result

def get_vaste_ul(vps):
    result = 0
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            vul = df_vestigingen.loc[int(vp), 'vaste_ul_vp']
            if pd.notna(vul):
                result += vul
        except:
            result += 0
    return result

def ul_asis(llngroepen):
    result = 0
    for vp, llng in llngroepen.items():
        if pd.notna(llng):
            for key, val in llng.items():
                result += val['uren-leraar']
    return result

def ul_tobe(llngroepen):
    result = 0
    for key, value in llngroepen.items():
        result += value['uren-leraar']
    return result

def get_directeurs(vps):
    result = 0
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            directeur = df_vestigingen.loc[int(vp), 'directeur_vp']
            if pd.notna(directeur):
                result += directeur
        except:
            result += 0
    return result

def get_lln_laatste_jaar(vps, aso):
    result = 0
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            if not aso:
                lln = df_vestigingen.loc[int(vp), 'lln_laatste_jaar']
            else:
                lln = df_vestigingen.loc[int(vp), 'lln_laatste_jaar_aso']
            if pd.notna(lln):
                result += lln
        except:
            result += 0
    return result

def get_ul_laatste_jaar(vps, aso):
    result = 0
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            if not aso:
                ul = df_vestigingen.loc[int(vp), 'ul_vp_laatste_jaar']
            else:
                ul = df_vestigingen.loc[int(vp), 'ul_vp_laatste_jaar_aso']
            if pd.notna(ul):
                result += ul
        except:
            result += 0
    return result

def get_dir_laatste_jaar(vps, aso):
    result = 0
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            if not aso:
                ul = df_vestigingen.loc[int(vp), 'dir_laatste_jaar']
            else:
                ul = df_vestigingen.loc[int(vp), 'dir_laatste_jaar_aso']
            if pd.notna(ul):
                result += ul
        except:
            result += 0
    return result

# De tabel is gebouwd op vestigingsplaatsen, dus er staan units meerdere keren in
df_units = df_units[['unit_code_so', 'unit_code_SO_actief']].drop_duplicates()

# Zoek bestuur en net op
df_units['schoolbestuur'] = df_units['unit_code_so'].apply(get_bestuur)
df_units['net'] = df_units['unit_code_so'].apply(get_net)

# Zoek leerlingengroepe as-is op en bereken to-be
df_units['llng_asis'] = df_units['unit_code_so'].apply(get_llngroepen_for_vestingsplaatsen)
df_units['llng_tobe'] = df_units['llng_asis'].apply(get_llngroepen_tobe)
df_units['leerlingengroepen'] = df_units['llng_asis'].apply(get_llngroepen_set)
df_units['aantal_leerlingen'] = df_units['llng_tobe'].apply(get_aantal_leerlingen)

# Kijk of er laatste graad van aso/tso/bso is
df_units['aso eind'] = df_units['leerlingengroepen'].apply(lambda llng: '3e graad aso' in llng)
df_units['tso eind'] = df_units['leerlingengroepen'].apply(lambda llng: '3e graad tso' in llng)
df_units['bso eind'] = df_units['leerlingengroepen'].apply(lambda llng: '3e graad bso' in llng or '4e graad bso' in llng)

# Groepeer de eindes voor analyse of DEA mogelijk is
df_eindes = df_units.groupby(['aso eind', 'tso eind', 'bso eind'])['unit_code_so'].count().reset_index().rename(columns={
    'unit_code_so': 'aantal units'
})

# Vaste uren-leraar leerlingengroepen
df_units['llngroep_ul_vast'] = df_units['unit_code_so'].apply(get_llngroep_vul)

# Bereken en vergelijk uren-leraar
df_units['ul_vast'] = df_units['unit_code_so'].apply(get_vaste_ul)
df_units['ul_asis'] = df_units['llng_asis'].apply(ul_asis)
df_units['ul_tobe'] = df_units['llng_tobe'].apply(ul_tobe)
df_units['ul_diff'] = df_units['ul_tobe'] - df_units['ul_asis']

df_units['ul_per_lln_asis'] = (df_units['ul_asis'] + df_units['ul_vast'])/df_units['aantal_leerlingen']
df_units['ul_per_lln_tobe'] = (df_units['ul_tobe'] + df_units['ul_vast'])/df_units['aantal_leerlingen']

# Bereken en vergelijk directeurs
df_units['directeurs_asis'] = df_units['unit_code_so'].apply(get_directeurs)
df_units['directeur_tobe'] = df_units.apply(lambda row: 1 if row['aantal_leerlingen'] > 0 else 0, axis=1)
df_units['directeur_diff'] = df_units['directeur_tobe'] - df_units['directeurs_asis']

df_units['lln_per_dir_asis'] = df_units['aantal_leerlingen']/df_units['directeurs_asis']
df_units['lln_per_dir_tobe'] = df_units['aantal_leerlingen']/df_units['directeur_tobe']

df_units['leerlingen_laatste_jaar'] = df_units.apply(
    lambda row: get_lln_laatste_jaar(row['unit_code_so'], False), axis=1)
df_units['uren-leraar_laatste_jaar'] = df_units.apply(
    lambda row: get_ul_laatste_jaar(row['unit_code_so'], False), axis=1)
df_units['directeurs_laatste_jaar'] = df_units.apply(
    lambda row: get_dir_laatste_jaar(row['unit_code_so'], False), axis=1)
df_units['leerlingen_laatste_jaar_aso'] = df_units.apply(
    lambda row: get_lln_laatste_jaar(row['unit_code_so'], True), axis=1)
df_units['uren-leraar_laatste_jaar_aso'] = df_units.apply(
    lambda row: get_ul_laatste_jaar(row['unit_code_so'], True), axis=1)
df_units['directeurs_laatste_jaar_aso'] = df_units.apply(
    lambda row: get_dir_laatste_jaar(row['unit_code_so'], True), axis=1)



with pd.ExcelWriter(f'output/jaren/{sys.argv[1]}/8_analyse_units.xlsx') as writer:
    df_units.to_excel(writer, sheet_name='Analyse', index=False)
    df_eindes.to_excel(writer, sheet_name='Eindes', index=False)