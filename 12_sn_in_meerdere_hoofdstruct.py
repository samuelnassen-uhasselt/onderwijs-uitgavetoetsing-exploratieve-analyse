import pandas as pd

file = "Brondata\\Inschrijvingen\\inschrijvingen-leerplicht-instellingen-dataset-2024-2025-1feb.xlsx"
df = pd.read_excel(file)

df = df[df['hoofdstructuur'].isin(['Buitengewoon secundair onderwijs', 'Deeltijds beroepssecundair onderwijs',
                                   'Syntra', 'Voltijds gewoon secundair onderwijs'])]
df = df.groupby(['instellingsnummer', 'hoofdstructuur'])['aantal_inschrijvingen'].sum().reset_index()

df_in = df.groupby('instellingsnummer')['hoofdstructuur'].count().reset_index()
df_in = df_in[df_in['hoofdstructuur']>1]

df = df[df['instellingsnummer'].isin(df_in['instellingsnummer'].values)].sort_values('instellingsnummer')
df.to_excel('output/12_sn_in_meerdere_hoofdstruct.xlsx', index=False)