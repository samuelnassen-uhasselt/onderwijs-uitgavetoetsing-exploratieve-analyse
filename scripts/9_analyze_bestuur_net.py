import pandas as pd
import sys

df_master = pd.read_excel(f'output/jaren/{sys.argv[1]}/5_master_ul_dir.xlsx')
df_units = pd.read_excel(f'output/jaren/{sys.argv[1]}/8_analyse_units.xlsx', sheet_name='Analyse')
df_units_met_inschrijvingen = df_units[df_units['aantal_leerlingen'] != 0]

# AS-IS situatie bestuur (op instellingsnummer)
df_bestuur_master = df_master.groupby(['schoolbestuur', 'schoolnummer']).size().reset_index()
df_bestuur_master = df_bestuur_master.groupby('schoolbestuur').agg(
    instellingen = ('schoolnummer', 'count'),
).reset_index()

# Filter units zonder bestuur
df_units_zonder_bestuur = df_units[df_units['schoolbestuur'] == '[]'].copy()

# TO-BE situatie bestuur (op units)
df_bestuur_units = df_units_met_inschrijvingen.groupby('schoolbestuur').agg(
    units = ('directeur_tobe', 'count'),
    aantal_leerlingen = ('aantal_leerlingen', 'sum'),
    ul_vast = ('ul_vast', 'sum'),
    ul_asis = ('ul_asis', 'sum'),
    ul_tobe = ('ul_tobe', 'sum'),
    ul_tobe_herwerkt = ('ul_tobe_herwerkt', 'sum'),
    ul_tobe_herwerkt_alle = ('ul_tobe_herwerkt_alle', 'sum'),
    directeur_asis = ('directeurs_asis', 'sum'),
    directeur_tobe = ('directeur_tobe', 'sum'),
    leerlingen_laatste_jaar = ('leerlingen_laatste_jaar', 'sum'),
    vaste_ul_laatste_jaar = ('vaste_uren-leraar_laatste_jaar', 'sum'),
    deg_ul_laatste_jaar_asis = ('deg_uren-leraar_laatste_jaar_asis', 'sum'),
    deg_ul_laatste_jaar_tobe = ('deg_uren-leraar_laatste_jaar_tobe', 'sum'),
    dir_laatste_jaar_asis = ('directeurs_laatste_jaar', 'sum'),
    leerlingen_laatste_jaar_aso = ('leerlingen_laatste_jaar_aso', 'sum'),
    vaste_ul_laatste_jaar_aso = ('vaste_uren-leraar_laatste_jaar_aso', 'sum'),
    deg_ul_laatste_jaar_aso_asis = ('deg_uren-leraar_laatste_jaar_aso_asis', 'sum'),
    deg_ul_laatste_jaar_aso_tobe = ('deg_uren-leraar_laatste_jaar_aso_tobe', 'sum'),
    dir_laatste_jaar_aso_asis = ('directeurs_laatste_jaar_aso', 'sum'),
).reset_index()

# Voeg as-is en to-be samen en bereken verschillen
df_bestuur = pd.merge(df_bestuur_master, df_bestuur_units, how='outer', on='schoolbestuur')
df_bestuur['ul_diff'] = df_bestuur['ul_tobe'] - df_bestuur['ul_asis']
df_bestuur['ul_diff_herwerkt'] = df_bestuur['ul_tobe_herwerkt'] - df_bestuur['ul_asis']
df_bestuur['ul_diff_in_euros_herwerkt'] = df_bestuur['ul_diff_herwerkt'] * 0.9657 * 69073 / 21.23
df_bestuur['ul_diff_herwerkt_alle'] = df_bestuur['ul_tobe_herwerkt_alle'] - df_bestuur['ul_asis']
df_bestuur['ul_diff_in_euros_herwerkt_alle'] = df_bestuur['ul_diff_herwerkt_alle'] * 0.9657 * 69073 / 21.23
df_bestuur['directeur_diff'] = df_bestuur['directeur_tobe'] - df_bestuur['directeur_asis']
df_bestuur = df_bestuur[['schoolbestuur', 'instellingen', 'units', 'aantal_leerlingen', 'ul_vast', 'ul_asis', 'ul_tobe', 
                         'ul_diff', 'ul_tobe_herwerkt', 'ul_diff_herwerkt', 'ul_diff_in_euros_herwerkt', 
                         'ul_tobe_herwerkt_alle', 'ul_diff_herwerkt_alle', 'ul_diff_in_euros_herwerkt_alle', 
                         'directeur_asis', 'directeur_tobe', 'directeur_diff', 'leerlingen_laatste_jaar', 'vaste_ul_laatste_jaar', 
                         'deg_ul_laatste_jaar_asis', 'deg_ul_laatste_jaar_tobe', 'dir_laatste_jaar_asis',
                         'leerlingen_laatste_jaar_aso', 'vaste_ul_laatste_jaar_aso', 'deg_ul_laatste_jaar_aso_asis',
                         'deg_ul_laatste_jaar_aso_tobe', 'dir_laatste_jaar_aso_asis',]]

df_bestuur['ul_per_lln_asis'] = (df_bestuur['ul_asis'] + df_bestuur['ul_vast'])/df_bestuur['aantal_leerlingen']
df_bestuur['ul_per_lln_tobe'] = (df_bestuur['ul_tobe'] + df_bestuur['ul_vast'])/df_bestuur['aantal_leerlingen']

df_bestuur['lln_per_dir_asis'] = df_bestuur['aantal_leerlingen']/df_bestuur['directeur_asis']
df_bestuur['lln_per_dir_tobe'] = df_bestuur['aantal_leerlingen']/df_bestuur['directeur_tobe']


# AS-IS situatie net (op instellingsnummer)
df_net_master = df_master.groupby(['net', 'schoolnummer']).size().reset_index()
df_net_master = df_net_master.groupby('net').agg(
    instellingen = ('schoolnummer', 'count'),
).reset_index()

# Filter units zonder net
df_units_zonder_net = df_units[df_units['net'] == '[]'].copy()

# TO-BE situatie net (op units)
df_net_units = df_units_met_inschrijvingen.groupby('net').agg(
    units = ('directeur_tobe', 'count'),
    aantal_leerlingen = ('aantal_leerlingen', 'sum'),
    ul_vast = ('ul_vast', 'sum'),
    ul_asis = ('ul_asis', 'sum'),
    ul_tobe = ('ul_tobe', 'sum'),
    ul_tobe_herwerkt = ('ul_tobe_herwerkt', 'sum'), 
    ul_tobe_herwerkt_alle = ('ul_tobe_herwerkt_alle', 'sum'),
    directeur_asis = ('directeurs_asis', 'sum'),
    directeur_tobe = ('directeur_tobe', 'sum')
).reset_index()

# Voeg as-is en to-be samen en bereken verschillen
df_net = pd.merge(df_net_master, df_net_units, how='outer', on='net')
df_net['ul_diff'] = df_net['ul_tobe'] - df_net['ul_asis']
df_net['ul_diff_herwerkt'] = df_net['ul_tobe_herwerkt'] - df_net['ul_asis']
df_net['ul_diff_in_euros_herwerkt'] = df_net['ul_diff_herwerkt'] * 0.9657 * 69073 / 21.23
df_net['ul_diff_herwerkt_alle'] = df_net['ul_tobe_herwerkt_alle'] - df_net['ul_asis']
df_net['ul_diff_in_euros_herwerkt_alle'] = df_net['ul_diff_herwerkt_alle'] * 0.9657 * 69073 / 21.23
df_net['directeur_diff'] = df_net['directeur_tobe'] - df_net['directeur_asis']
df_net = df_net[['net', 'instellingen', 'units', 'aantal_leerlingen', 'ul_vast', 'ul_asis', 'ul_tobe', 'ul_diff',
                 'ul_tobe_herwerkt', 'ul_diff_herwerkt', 'ul_diff_in_euros_herwerkt', 
                 'ul_tobe_herwerkt_alle', 'ul_diff_herwerkt_alle', 'ul_diff_in_euros_herwerkt_alle',
                 'directeur_asis', 'directeur_tobe', 'directeur_diff']]

df_net['ul_per_lln_asis'] = (df_net['ul_asis'] + df_net['ul_vast'])/df_net['aantal_leerlingen']
df_net['ul_per_lln_tobe'] = (df_net['ul_tobe'] + df_net['ul_vast'])/df_net['aantal_leerlingen']

df_net['lln_per_dir_asis'] = df_net['aantal_leerlingen']/df_net['directeur_asis']
df_net['lln_per_dir_tobe'] = df_net['aantal_leerlingen']/df_net['directeur_tobe']



with pd.ExcelWriter(f'output/jaren/{sys.argv[1]}/9_analyse_bestuur_net.xlsx') as writer:
    df_net.to_excel(writer, sheet_name='NET', index=False)
    df_units_zonder_net.to_excel(writer, sheet_name='Units zonder net', index=False)
    df_bestuur.to_excel(writer, sheet_name='BESTUUR', index=False)
    df_units_zonder_bestuur.to_excel(writer, sheet_name='Units zonder bestuur', index=False)