import ast
import numpy as np
import pandas as pd
import degressieve_ul_llngroepen as dul
from scipy.spatial.distance import pdist
import sys
import math

df_units = pd.read_excel('Brondata\\Units en complexen\\SO_complexen_DLinfo.xlsx')
df_master = pd.read_excel(f'output/jaren/{sys.argv[1]}/5_master_ul_dir.xlsx')
df_master_lookup = df_master.copy().set_index('vestigingsplaats')
df_laatste_jaar = pd.read_excel(f'output/jaren/{sys.argv[1]}/1_inschrijvingen_vestigingen.xlsx', sheet_name='Laatste Jaar')
df_laatste_jaar.set_index('vestigingsplaats', inplace=True)

def get_max_afstand(vps):
    coords = []
    vps = vps.replace('SO', '')
    for vp in vps.split('_'):
        try:
            x = df_master_lookup.loc[int(vp), 'lx']
            y = df_master_lookup.loc[int(vp), 'ly']
            if pd.notna(x) and pd.notna(y):
                coords.append((x, y))
        except:
            continue

    afstand = pdist(np.array(list(coords))).max() if len(coords) > 1 else 0
    return round(afstand/1000, 2)

def get_bestuur(vps):
    result = []
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            bestuur = df_master_lookup.loc[int(vp), 'schoolbestuur']
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
            net = df_master_lookup.loc[int(vp), 'net']
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
            llngroep = df_master_lookup.loc[int(vp), 'ul_llngroepen']
            if pd.notna(llngroep):
                llngroep = ast.literal_eval(llngroep)
            result[vp] = (llngroep)
        except:
            result[vp] = np.nan

    return result

def get_llngroepen_tobe(llngroepen_asis, herwerkt):
    result = {}
    for vp, llng in llngroepen_asis.items():
        if pd.notna(llng):
            for key, value in llng.items():
                if key not in result:
                    result[key] = {'inschrijvingen': 0}
                result[key]['inschrijvingen'] += value['inschrijvingen']

    for key, value in result.items():
        result[key]['ul'] = dul.get_degressieve_uren_leraar(key, value['inschrijvingen'], herwerkt)
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
            llngroep = df_master_lookup.loc[int(vp), 'leerlingengroepen_vaste_ul_vp']
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
            vul = df_master_lookup.loc[int(vp), 'vaste_ul_vp']
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
                result += val['ul']
    return result

def ul_tobe(llngroepen):
    result = 0
    for key, value in llngroepen.items():
        result += value['ul']
    return result

def get_directeurs(vps):
    result = 0
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            directeur = df_master_lookup.loc[int(vp), 'directeur_vp']
            if pd.notna(directeur):
                result += directeur
        except:
            result += 0
    return result

def get_directeur_tobe(llngr, aantal):
    g = '_'.join(llngr.keys())
    if '3e graad' in g or '4e graad' in g or 'hbo' in g or 'n.v.t. (modulair) bso' in g:
        if aantal >= 83:
            return 1
        return 0
    if aantal >= 120:
        return 1
    return 0

def get_lln_laatste_jaar(vps, aso):
    result = 0
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            if not aso:
                lln = df_master_lookup.loc[int(vp), 'lln_laatste_jaar']
            else:
                lln = df_master_lookup.loc[int(vp), 'lln_laatste_jaar_aso']
            if pd.notna(lln):
                result += lln
        except:
            result += 0
    return result

def get_ul_laatste_jaar_asis(vps, aso):
    vast = 0
    deg = 0
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            if not aso:
                v, d = df_master_lookup.loc[int(vp), ['ul_vast_vp_laatste_jaar', 'ul_deg_asis_vp_laatste_jaar']]
            else:
                v, d = df_master_lookup.loc[int(vp), ['ul_vast_vp_laatste_jaar_aso', 'ul_deg_asis_vp_laatste_jaar_aso']]
            if pd.notna(v):
                vast += v
            if pd.notna(d):
                deg += d
        except:
            pass
    return pd.Series([vast, deg])

def get_ul_deg_laatste_jaar_tobe(vps, ul_llngr):
    result = {}
    sum = 0
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            llngr_lj = df_laatste_jaar.loc[[int(vp)]]
        except:
            continue
        llngr_lj = llngr_lj.to_dict('records')
        for llngr in llngr_lj:
            tot_lln = ul_llngr[llngr['leerlingengroep']]['inschrijvingen']
            lln_lj = llngr['aantal_inschrijvingen']
            ul_deg_vp = ul_llngr[llngr['leerlingengroep']]['ul']
            ul_deg_lj = lln_lj*ul_deg_vp/tot_lln
            sum += ul_deg_lj
            if llngr['leerlingengroep'] not in result.keys():
                result[llngr['leerlingengroep']] = {'inschrijvingen': 0, 'ul': 0}
            result[llngr['leerlingengroep']]['inschrijvingen'] += lln_lj
            result[llngr['leerlingengroep']]['ul'] += ul_deg_lj
    return pd.Series([result, sum])

def get_ul_deg_laatste_jaar_aso_tobe(llngr):
    try:
        return llngr['3e graad aso']['ul']
    except:
        return 0

def get_dir_laatste_jaar(vps, aso):
    result = 0
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            if not aso:
                dir = df_master_lookup.loc[int(vp), 'dir_laatste_jaar']
            else:
                dir = df_master_lookup.loc[int(vp), 'dir_laatste_jaar_aso']
            if pd.notna(dir):
                result += dir
        except:
            result += 0
    return result

def get_extra_aanwendbaar(vps, laatste, aso):
    ul, ambten, punten = [0,0,0]
    vps = vps.replace('SO_', '')
    for vp in vps.split('_'):
        try:
            if not aso:
                if laatste:
                    extra = df_master_lookup.loc[int(vp), ['extra_ul_aanwendbaar_laatste', 
                                                           'extra_ambten_aanwendbaar_laatste', 'extra_punten_aanwendbaar_laatste']]
                else:
                    extra = df_master_lookup.loc[int(vp), ['extra_ul_aanwendbaar', 
                                                           'extra_ambten_aanwendbaar', 'extra_punten_aanwendbaar']]
            else:
                extra = df_master_lookup.loc[int(vp), ['extra_ul_aanwendbaar_laatste_aso', 
                                                       'extra_ambten_aanwendbaar_laatste_aso', 
                                                       'extra_punten_aanwendbaar_laatste_aso']]
            ul += extra.iloc[0]
            ambten += extra.iloc[1]
            punten += extra.iloc[2]
        except:
            continue

    return pd.Series([ul, ambten, punten])

def get_punten_directeurs_tobe_herwerkt(aantal):
    return math.floor(aantal/375)*120

# De tabel is gebouwd op vestigingsplaatsen, dus er staan units meerdere keren in
df_units = df_units[['unit_code_so', 'unit_code_SO_actief']].drop_duplicates()

df_units['max_afstand_km'] = df_units['unit_code_so'].apply(get_max_afstand)

# Zoek bestuur en net op
df_units['schoolbestuur'] = df_units['unit_code_so'].apply(get_bestuur)
df_units['net'] = df_units['unit_code_so'].apply(get_net)

# Zoek leerlingengroepe as-is op en bereken to-be
df_units['llng_asis'] = df_units['unit_code_so'].apply(get_llngroepen_for_vestingsplaatsen)
df_units['llng_tobe'] = df_units.apply(lambda row: get_llngroepen_tobe(row['llng_asis'], herwerkt=None), axis=1)
df_units['llng_tobe_herwerkt'] = df_units.apply(lambda row: get_llngroepen_tobe(row['llng_asis'], herwerkt='DEEL'), axis=1)
df_units['llng_tobe_herwerkt_alle'] = df_units.apply(lambda row: get_llngroepen_tobe(row['llng_asis'], herwerkt='ALLE'), axis=1)
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
df_units['ul_tobe_herwerkt'] = df_units['llng_tobe_herwerkt'].apply(ul_tobe)
df_units['ul_diff_herwerkt'] = df_units['ul_tobe_herwerkt'] - df_units['ul_asis']
df_units['ul_diff_in_euros_herwerkt'] = df_units['ul_diff_herwerkt'] * 0.9657 * 69073 / 21.23
df_units['ul_tobe_herwerkt_alle'] = df_units['llng_tobe_herwerkt_alle'].apply(ul_tobe)
df_units['ul_diff_herwerkt_alle'] = df_units['ul_tobe_herwerkt_alle'] - df_units['ul_asis']
df_units['ul_diff_in_euros_herwerkt_alle'] = df_units['ul_diff_herwerkt_alle'] * 0.9657 * 69073 / 21.23

df_units['ul_per_lln_asis'] = (df_units['ul_asis'] + df_units['ul_vast'])/df_units['aantal_leerlingen']
df_units['ul_per_lln_tobe'] = (df_units['ul_tobe'] + df_units['ul_vast'])/df_units['aantal_leerlingen']

# Bereken en vergelijk directeurs
df_units['directeurs_asis'] = df_units['unit_code_so'].apply(get_directeurs)
df_units['directeur_tobe'] = df_units.apply(lambda row: get_directeur_tobe(row['llng_tobe'],
                                                                           row['aantal_leerlingen']), axis=1)
df_units['directeur_diff'] = df_units['directeur_tobe'] - df_units['directeurs_asis']

df_units['lln_per_dir_asis'] = df_units['aantal_leerlingen']/df_units['directeurs_asis']
df_units['lln_per_dir_tobe'] = df_units['aantal_leerlingen']/df_units['directeur_tobe']

df_units['leerlingen_laatste_jaar'] = df_units.apply(
    lambda row: get_lln_laatste_jaar(row['unit_code_so'], False), axis=1)
df_units[['vaste_uren-leraar_laatste_jaar', 'deg_uren-leraar_laatste_jaar_asis']] = df_units.apply(
    lambda row: get_ul_laatste_jaar_asis(row['unit_code_so'], False), axis=1)
df_units[['llngr_laatste_jaar_tobe', 'deg_uren-leraar_laatste_jaar_tobe']] = df_units.apply(
    lambda row: get_ul_deg_laatste_jaar_tobe(row['unit_code_so'], row['llng_tobe']), axis=1)
df_units['directeurs_laatste_jaar'] = df_units.apply(
    lambda row: get_dir_laatste_jaar(row['unit_code_so'], False), axis=1)
df_units['leerlingen_laatste_jaar_aso'] = df_units.apply(
    lambda row: get_lln_laatste_jaar(row['unit_code_so'], True), axis=1)
df_units[['vaste_uren-leraar_laatste_jaar_aso', 'deg_uren-leraar_laatste_jaar_aso_asis']] = df_units.apply(
    lambda row: get_ul_laatste_jaar_asis(row['unit_code_so'], True), axis=1)
df_units['deg_uren-leraar_laatste_jaar_aso_tobe'] = df_units['llngr_laatste_jaar_tobe'].apply(
    get_ul_deg_laatste_jaar_aso_tobe)
df_units['directeurs_laatste_jaar_aso'] = df_units.apply(
    lambda row: get_dir_laatste_jaar(row['unit_code_so'], True), axis=1)

df_units[['extra_ul_aanwendbaar', 'extra_ambten_aanwendbaar', 'extra_punten_aanwendbaar']] = df_units.apply(
    lambda row: get_extra_aanwendbaar(row['unit_code_so'], False, False),
    axis=1
)
df_units[['extra_ul_aanwendbaar_laatste', 'extra_ambten_aanwendbaar_laatste', 'extra_punten_aanwendbaar_laatste']] = df_units.apply(
    lambda row: get_extra_aanwendbaar(row['unit_code_so'], True, False),
    axis=1
)
df_units[['extra_ul_aanwendbaar_laatste_aso', 'extra_ambten_aanwendbaar_laatste_aso', 'extra_punten_aanwendbaar_laatste_aso']] = df_units.apply(
    lambda row: get_extra_aanwendbaar(row['unit_code_so'], True, True),
    axis=1
)
df_units['punten_dir_tobe_herwerkt'] = df_units['aantal_leerlingen'].apply(get_punten_directeurs_tobe_herwerkt)

with pd.ExcelWriter(f'output/jaren/{sys.argv[1]}/8_analyse_units.xlsx') as writer:
    df_units.to_excel(writer, sheet_name='Analyse', index=False)
    df_eindes.to_excel(writer, sheet_name='Eindes', index=False)



df_units['vestigingsplaats'] = df_units['unit_code_so'].str.replace('SO_', '').str.split('_')
df_unit_lookup = df_units.explode('vestigingsplaats')
df_unit_lookup = df_unit_lookup.set_index('vestigingsplaats').sort_index()

def get_tobe_vp(vp, master_llngr, laatste):
    result = {}
    tot = 0
    try:
        unit = df_unit_lookup.loc[str(vp)]
        if laatste:
            llngr = unit['llngr_laatste_jaar_tobe']
        else:
            llngr = unit['llng_tobe']
        for groep, inschr in ast.literal_eval(master_llngr).items():
            tobe = llngr[groep]
            if groep not in result:
                result[groep] = {'inschrijvingen': 0, 'ul': 0}
            result[groep]['inschrijvingen'] += inschr
            deg_ul_tobe = tobe['ul'] * inschr/tobe['inschrijvingen']
            result[groep]['ul'] = deg_ul_tobe
            tot += deg_ul_tobe
    except:
        pass
    return pd.Series([result, tot])

def get_dir_vp_tobe(vp, lln):
    try:
        unit = df_unit_lookup.loc[str(vp)]
        lln_unit = unit['aantal_leerlingen']
        dir_unit = unit['directeur_tobe']
        if pd.notna(lln_unit) and lln_unit != 0:
            return lln*dir_unit/lln_unit
        else:
            return 0
    except:
        return 0

def get_aso_ul_vp(llngr):
    try:
        return llngr['3e graad aso']['ul']
    except:
        return 0


df_master[['llngr_tobe', 'ul_tobe']] = df_master.apply(lambda row:
    get_tobe_vp(row['vestigingsplaats'], row['leerlingengroepen_vp'], False), axis=1)
df_master['directeurs_tobe'] = df_master.apply(lambda row:
    get_dir_vp_tobe(row['vestigingsplaats'], row['aantal_inschrijvingen_vp']), axis=1)
df_master[['llngr_laatste_jaar_tobe', 'ul_laatste_jaar_tobe']] = df_master.apply(lambda row:
    get_tobe_vp(row['vestigingsplaats'], row['llngroepen_laatste_jaar'], True), axis=1)
df_master['directeurs_laatste_jaar_tobe'] = df_master.apply(lambda row:
    get_dir_vp_tobe(row['vestigingsplaats'], row['lln_laatste_jaar']), axis=1)
df_master['ul_laatste_jaar_aso_tobe'] = df_master['llngr_laatste_jaar_tobe'].apply(get_aso_ul_vp)
df_master['directeurs_laatste_jaar_aso_tobe'] = df_master.apply(lambda row:
    get_dir_vp_tobe(row['vestigingsplaats'], row['lln_laatste_jaar_aso']), axis=1)

df_master.to_excel(f'output/jaren/{sys.argv[1]}/5_master_ul_dir.xlsx', index=False)