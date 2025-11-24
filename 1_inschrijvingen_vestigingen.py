import pandas as pd
import vaste_ul as vul

inschrijvingen = "Brondata\\Inschrijvingen\\inschrijvingen-leerplicht-instellingen-dataset-2024-2025-1feb.xlsx"

df = pd.read_excel(inschrijvingen)
df = df[df['hoofdstructuur'] == 'Voltijds gewoon secundair onderwijs']

# Groepeer en tel aantal inschrijvingen
df = df.groupby([
    'instellingsnummer', 'intern_volgnr_vpl', 'vestigingsplaats_adres', 'onderwijsvorm', 'graad_so', 'leerjaar_code', 'schoolbestuur', 'onderwijsnet', 'studierichting'
]).agg({
        'aantal_inschrijvingen': 'sum'
}).reset_index()

# Maak nieuwe kolommen
# Definieer leerlingengroep A/B aan de hand van leerjaren voor eerste graad (1A/B, 2A/B)
df['vestigingsplaats'] = df['instellingsnummer'].astype(str) + df['intern_volgnr_vpl'].astype(str).str.zfill(2)
df['leerlingengroep'] = df.apply(lambda row: f'{row['graad_so']} {row['leerjaar_code'][-1]}'
                                 if row['graad_so'] == '1e graad'
                                 else 'hbo'
                                 if row['graad_so'] == 'n.v.t. (hbo)'
                                 else f'{row['graad_so']} {row['onderwijsvorm']}', 
                                 axis=1)
df['vaste_ul'] = df.apply(lambda row: vul.get_ul(
    row['studierichting'], row['leerlingengroep'], row['aantal_inschrijvingen']
), axis= 1)

df.to_excel('1b_vaste_ul_stdr.xlsx', index=False)

# Groepeer op leerlingengroep om de leerjaren samen te nemen
df = df.groupby(['vestigingsplaats', 'vestigingsplaats_adres', 'leerlingengroep', 'schoolbestuur', 'onderwijsnet']).agg({
    'aantal_inschrijvingen': 'sum',
    'vaste_ul': 'sum'
}).reset_index()

# Neem alles samen op vestigingsplaats
# De leerlingengroepen met bijhorende inschrijvingen komen terecht in een lijst
df = df.groupby(['vestigingsplaats', 'vestigingsplaats_adres', 'schoolbestuur', 'onderwijsnet']).agg(
    leerlingengroepen=('leerlingengroep', lambda x: dict(zip(x, df.loc[x.index, 'aantal_inschrijvingen']))),
    leerlingengroepen_vaste_ul = ('leerlingengroep', lambda x: dict(zip(x, df.loc[x.index, 'vaste_ul']))),
    aantal_inschrijvingen=('aantal_inschrijvingen', 'sum'),
    vaste_ul=('vaste_ul', 'sum')
).reset_index()

df.to_excel('1a_inschrijvingen_vestigingsplaatsen_llngroepen_aantal-24-25.xlsx', index=False)