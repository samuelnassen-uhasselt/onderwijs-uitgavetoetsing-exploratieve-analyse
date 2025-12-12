import pandas as pd
import sys

df = pd.read_excel(f'output/jaren/{sys.argv[1]}/10_vergelijkbare_scholen.xlsx')

df = df.groupby(['c_aantal_leerlingen', 'c_leerlingengroepen']).agg(
    aantal_adressen = ('adres', 'count'),
    leerlingen_avg = ('aantal_leerlingen', 'mean'),
    splitsing_min = ('gesplitste_leerlingengroepen', 'min'),
    spitsing_max = ('gesplitste_leerlingengroepen', 'max'),
    spitsing_avg = ('gesplitste_leerlingengroepen', 'mean'),
    ul_meeste_winst = ('ul_diff', 'max'),
    ul_meeste_verlies = ('ul_diff', 'min'),
    ul_avg = ('ul_diff', 'mean'),
    OGO_ul_diff_avg = ('ul_diff', lambda x: x[df.loc[x.index, 'net'] == 'Officieel gesubsidieerd onderwijs'].mean()),
    GO_ul_diff_avg = ('ul_diff', lambda x: x[df.loc[x.index, 'net'] == 'Gemeenschapsonderwijs'].mean()),
    VGO_ul_diff_avg = ('ul_diff', lambda x: x[df.loc[x.index, 'net'] == 'Vrij gesubsidieerd onderwijs'].mean()),
    dir_meeste_winst = ('directeur_diff', 'max'),
    dir_meeste_verlies = ('directeur_diff', 'min'),
    dir_avg = ('directeur_diff', 'mean'),
    OGO_dir_diff_avg = ('directeur_diff', lambda x: x[df.loc[x.index, 'net'] == 'Officieel gesubsidieerd onderwijs'].mean()),
    GO_dir_diff_avg = ('directeur_diff', lambda x: x[df.loc[x.index, 'net'] == 'Gemeenschapsonderwijs'].mean()),
    VGO_dir_diff_avg = ('directeur_diff', lambda x: x[df.loc[x.index, 'net'] == 'Vrij gesubsidieerd onderwijs'].mean()),

    
).reset_index()

df.to_excel(f'output/jaren/{sys.argv[1]}/11_analyse_clusters_vergelijkbaar.xlsx', index=False)