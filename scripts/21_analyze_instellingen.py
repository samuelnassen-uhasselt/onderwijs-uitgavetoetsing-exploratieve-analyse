import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
import sys

df_master = pd.read_excel(f'output/jaren/{sys.argv[1]}/5_master_ul_dir.xlsx')
df_zelfde_adres = pd.read_excel(f'output/jaren/{sys.argv[1]}/6_zelfde_adres.xlsx', sheet_name='Scholen Zelfde Adres')
df_zelfde_adres = df_zelfde_adres.set_index('vestigingsplaats_1')

def check_if_in_zelfde_adres(vp):
    try:
        df_zelfde_adres.loc[(vp)]
        return True
    except:
        return False

df_master['deelt_adres'] = df_master['vestigingsplaats'].apply(check_if_in_zelfde_adres)

df_master_lookup = df_master.copy().set_index('vestigingsplaats')

df_instellingen = df_master.groupby('schoolnummer').agg({
    'vestigingsplaats': lambda x: '_'.join(x.astype(str)),
    'deelt_adres': 'sum',
    'aantal_inschrijvingen_vp': 'sum',
    'vaste_ul_vp': 'sum',
    'ul_vp': 'sum',
    'ul_tobe': 'sum',
    'directeurs_tobe': 'sum',
    'lln_laatste_jaar': 'sum',
    'ul_vast_vp_laatste_jaar': 'sum',
    'ul_deg_asis_vp_laatste_jaar': 'sum',
    'ul_laatste_jaar_tobe': 'sum',
    'dir_laatste_jaar': 'sum',
    'directeurs_laatste_jaar_tobe': 'sum',
    'lln_laatste_jaar_aso': 'sum',
    'ul_vast_vp_laatste_jaar_aso': 'sum',
    'ul_deg_asis_vp_laatste_jaar_aso': 'sum',
    'ul_laatste_jaar_aso_tobe': 'sum',
    'dir_laatste_jaar_aso': 'sum',
    'directeurs_laatste_jaar_aso_tobe': 'sum',
    'extra_ul_aanwendbaar': 'sum',
    'extra_ambten_aanwendbaar': 'sum',
    'extra_punten_aanwendbaar': 'sum',
    'extra_ul_aanwendbaar_laatste': 'sum',
    'extra_ambten_aanwendbaar_laatste': 'sum',
    'extra_punten_aanwendbaar_laatste': 'sum',
    'extra_ul_aanwendbaar_laatste_aso': 'sum',
    'extra_ambten_aanwendbaar_laatste_aso': 'sum',
    'extra_punten_aanwendbaar_laatste_aso': 'sum',
}).reset_index()

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

df_instellingen['max_afstand_km'] = df_instellingen['vestigingsplaats'].apply(get_max_afstand)

df_instellingen.to_excel(f'output/jaren/{sys.argv[1]}/21_analyse_instellingen.xlsx', index=False)