import pandas as pd

df_master = pd.read_excel('output/5_master_ul_dir.xlsx')
df_units = pd.read_excel('output/8a_analyse_units.xlsx')
df_units_met_inschrijvingen = df_units[df_units['aantal_leerlingen'] != 0]

# AS-IS situatie bestuur (op instellingsnummer)
df_bestuur_master = df_master.groupby(['schoolbestuur', 'schoolnummer'])[['vaste_ul', 'ul_vp', 'directeur_vp', 'aantal_inschrijvingen_vp']].sum().reset_index()
df_bestuur_master = df_bestuur_master.groupby('schoolbestuur').agg(
    instellingen = ('schoolnummer', 'count'),
    aantal_leerlingen = ('aantal_inschrijvingen_vp', 'sum'),
    ul_vast = ('vaste_ul', 'sum'),
    ul_asis = ('ul_vp', 'sum'),
    directeur_asis = ('directeur_vp', 'sum')
).reset_index()

# Filter units zonder bestuur
df_units[df_units['schoolbestuur'] == '[]'].to_excel('output/9c_units_zonder_bestuur.xlsx', index=False)

# TO-BE situatie bestuur (op units)
df_bestuur_units = df_units_met_inschrijvingen.groupby('schoolbestuur').agg(
    units = ('directeur_tobe', 'count'),
    ul_tobe = ('ul_tobe', 'sum'),
    directeur_tobe = ('directeur_tobe', 'sum')
).reset_index()

# Voeg as-is en to-be samen en bereken verschillen
df_bestuur = pd.merge(df_bestuur_master, df_bestuur_units, how='outer', on='schoolbestuur')
df_bestuur['ul_diff'] = df_bestuur['ul_tobe'] - df_bestuur['ul_asis']
df_bestuur['directeur_diff'] = df_bestuur['directeur_tobe'] - df_bestuur['directeur_asis']
df_bestuur = df_bestuur[['schoolbestuur', 'instellingen', 'units', 'aantal_leerlingen', 'ul_vast', 
                         'ul_asis', 'ul_tobe', 'ul_diff', 'directeur_asis', 'directeur_tobe', 'directeur_diff']]

df_bestuur['ul_per_lln_asis'] = (df_bestuur['ul_asis'] + df_bestuur_master['ul_vast'])/df_bestuur['aantal_leerlingen']
df_bestuur['ul_per_lln_tobe'] = (df_bestuur['ul_tobe'] + df_bestuur_master['ul_vast'])/df_bestuur['aantal_leerlingen']

df_bestuur['lln_per_dir_asis'] = df_bestuur['aantal_leerlingen']/df_bestuur['directeur_asis']
df_bestuur['lln_per_dir_tobe'] = df_bestuur['aantal_leerlingen']/df_bestuur['directeur_tobe']

df_bestuur.to_excel('output/9a_analyse_bestuur.xlsx', index=False)


# AS-IS situatie net (op instellingsnummer)
df_net_master = df_master.groupby(['net', 'schoolnummer'])[['vaste_ul', 'ul_vp', 'directeur_vp', 'aantal_inschrijvingen_vp']].sum().reset_index()
df_net_master = df_net_master.groupby('net').agg(
    instellingen = ('schoolnummer', 'count'),
    aantal_leerlingen = ('aantal_inschrijvingen_vp', 'sum'),
    ul_vast = ('vaste_ul', 'sum'),
    ul_asis = ('ul_vp', 'sum'),
    directeur_asis = ('directeur_vp', 'sum')
).reset_index()

# Filter units zonder net
df_units[df_units['net'] == '[]'].to_excel('output/9d_units_zonder_net.xlsx', index=False)

# TO-BE situatie net (op units)
df_net_units = df_units_met_inschrijvingen.groupby('net').agg(
    units = ('directeur_tobe', 'count'),
    ul_tobe = ('ul_tobe', 'sum'),
    directeur_tobe = ('directeur_tobe', 'sum')
).reset_index()

# Voeg as-is en to-be samen en bereken verschillen
df_net = pd.merge(df_net_master, df_net_units, how='outer', on='net')
df_net['ul_diff'] = df_net['ul_tobe'] - df_net['ul_asis']
df_net['directeur_diff'] = df_net['directeur_tobe'] - df_net['directeur_asis']
df_net = df_net[['net', 'instellingen', 'units', 'aantal_leerlingen', 'ul_vast', 
                 'ul_asis', 'ul_tobe', 'ul_diff', 'directeur_asis', 'directeur_tobe', 'directeur_diff']]

df_net['ul_per_lln_asis'] = (df_net['ul_asis'] + df_net['ul_vast'])/df_net['aantal_leerlingen']
df_net['ul_per_lln_tobe'] = (df_net['ul_tobe'] + df_net['ul_vast'])/df_net['aantal_leerlingen']

df_net['lln_per_dir_asis'] = df_net['aantal_leerlingen']/df_net['directeur_asis']
df_net['lln_per_dir_tobe'] = df_net['aantal_leerlingen']/df_net['directeur_tobe']

df_net.to_excel('output/9b_analyse_net.xlsx', index=False)