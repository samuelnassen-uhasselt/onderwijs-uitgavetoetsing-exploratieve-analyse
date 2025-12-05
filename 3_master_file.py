import pandas as pd
import numpy as np
import sys

vpl_info = pd.read_excel(f'jaren/{sys.argv[1]}/0_vestigingsplaatsen_volledig_nummer.xlsx')
vpl_inschrijvingen = pd.read_excel(f'jaren/{sys.argv[1]}/1a_inschrijvingen_vestigingsplaatsen_llngroepen_aantal.xlsx')
besturen = pd.read_excel(f'jaren/{sys.argv[1]}/2_besturen.xlsx')
bestuur_op_nummer = besturen.set_index('nummer_im')
bestuur_op_naam = besturen.set_index('naam_im')
df_sn_bn = vpl_info[['bestuur', 'schoolnummer']].drop_duplicates().set_index('schoolnummer')

net_kort_naar_lang = {
    'OGO': 'Officieel gesubsidieerd onderwijs',
    'VGO': 'Vrij gesubsidieerd onderwijs',
    'GO': 'Gemeenschapsonderwijs'
}

def get_bestuurnummer(bn, sn, naam):
    if pd.notna(sn):
        try:
            return df_sn_bn.loc[sn, 'bestuur']
        except:
            try:
                if naam == 'vzw Sint-Paulusschool':
                    return 114207
                if naam == 'Hasp-O Centrum':
                    return 108324
                if naam == 'VZW OZCS Midden-Kempen':
                    return 123398
                if naam == 'SKOBO':
                    return 971226
                if naam == 'GO! scholengroep SAM':
                    return 113936
                return bestuur_op_naam.loc[naam, 'nummer_im']
            except:
                if pd.notna(bn):
                    return bn
                return
    return bn

def get_bestuurnaam(nummer, naam):
    if nummer == 963165:
        return 'VZW Sint-Michielscollege Brasschaat'
    if nummer == 974261:
        return 'VZW Sint-Michielscollege Schoten'
    if pd.notna(nummer):
        try:
            return bestuur_op_nummer.loc[nummer, 'naam_im']
        except:
            if pd.notna(naam):
                return naam
            return
    return naam

def get_lambert(adres):
    url = 'https://loc.geopunt.be/v4/location'

# Merge en selecteer kolommen
df_master = pd.merge(vpl_info, vpl_inschrijvingen, how='outer', on='vestigingsplaats')
df_master['schoolnummer'] = df_master['vestigingsplaats'].astype(str).str[:-2].astype(int)

# Zoek het nummer van het bestuur op waar mogelijk
df_master['bestuur'] = df_master.apply(
    lambda row: get_bestuurnummer(row['bestuur'], row['schoolnummer'], row['schoolbestuur']), axis=1
)

# Zoek de naam van het bestuur waar mogelijk
df_master['schoolbestuur'] = df_master.apply(
    lambda row: get_bestuurnaam(row['bestuur'], row['schoolbestuur']), axis=1
)

# Twee waardes voor net. Afkorting en volledig. Neem de volledig uitgeschreven versie en vul aan waar nodig.
df_master['net'] = df_master.apply(
    lambda row: row['net'] if pd.notna(row['net']) else net_kort_naar_lang[row['onderwijsnet']]
        if pd.notna(row['onderwijsnet']) else np.nan, axis=1
)

# Selecteer kolommen
df_master = df_master[['vestigingsplaats', 'vestigingsplaats_adres', 'provincie', 'lx', 'ly', 
                       'bestuur', 'schoolbestuur', 'net', 'onderwijsnet', 'schoolnummer', 'leerlingengroepen',
                       'leerlingengroepen_vaste_ul', 'aantal_inschrijvingen', 'vaste_ul']]


df_master.to_excel(f'jaren/{sys.argv[1]}/3_vestigingsplaatsen_master.xlsx', index=False)