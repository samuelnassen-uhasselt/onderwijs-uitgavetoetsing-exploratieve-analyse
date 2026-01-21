import pandas as pd
import vaste_ul as vul
import sys

def get_leerlingengroep(graad, leerjaar, ov):
    if graad == '1e graad':
        if leerjaar == 'BV':
            return f'{graad} {leerjaar}'
        else:
            return f'{graad} {leerjaar[-1]}'
    if graad == 'n.v.t. (hbo)':
        return 'hbo'
    return f'{graad} {ov}'

inschrijvingen = f"Brondata\\Inschrijvingen\\inschrijvingen-leerplicht-instellingen-dataset-{sys.argv[1]}-1feb.xlsx"

df = pd.read_excel(inschrijvingen)
df = df[df['hoofdstructuur'] == 'Voltijds gewoon secundair onderwijs']

# Groepeer en tel aantal inschrijvingen
df = df.groupby([
    'instellingsnummer', 'intern_volgnr_vpl', 'vestigingsplaats_adres', 'onderwijsvorm', 'graad_so', 
    'leerjaar_code', 'schoolbestuur', 'onderwijsnet', 'scholengemeenschap', 'studierichting'
]).agg({
        'aantal_inschrijvingen': 'sum'
}).reset_index()

# Maak nieuwe kolommen
# Definieer leerlingengroep A/B aan de hand van leerjaren voor eerste graad (1A/B, 2A/B)
df['vestigingsplaats'] = df['instellingsnummer'].astype(str) + df['intern_volgnr_vpl'].astype(str).str.zfill(2)
df['leerlingengroep'] = df.apply(lambda row: 
                                 get_leerlingengroep(row['graad_so'], row['leerjaar_code'], row['onderwijsvorm']), 
                                 axis=1)
df['vaste_ul'] = df.apply(lambda row: vul.get_ul(
    row['studierichting'], row['leerlingengroep'], row['aantal_inschrijvingen']
), axis= 1)

df_vul_stdr = df.copy()

df_laaste_jaar = df[df['graad_so'].isin(['3e graad', 'n.v.t. (hbo)'])]
df_laaste_jaar = df_laaste_jaar[df_laaste_jaar['leerjaar_code'].isin(['2', '3', '/'])]
df_laaste_jaar = df_laaste_jaar.groupby(['vestigingsplaats', 'leerlingengroep'])[[
    'aantal_inschrijvingen', 'vaste_ul']].sum().reset_index()

# Groepeer op leerlingengroep om de leerjaren samen te nemen
df = df.groupby(['vestigingsplaats', 'vestigingsplaats_adres', 'leerlingengroep', 
                 'schoolbestuur', 'onderwijsnet', 'scholengemeenschap']).agg({
    'aantal_inschrijvingen': 'sum',
    'vaste_ul': 'sum'
}).reset_index()

# Neem alles samen op vestigingsplaats
# De leerlingengroepen met bijhorende inschrijvingen komen terecht in een lijst
df = df.groupby(['vestigingsplaats', 'vestigingsplaats_adres', 'schoolbestuur', 'onderwijsnet', 'scholengemeenschap']).agg(
    leerlingengroepen=('leerlingengroep', lambda x: dict(zip(x, df.loc[x.index, 'aantal_inschrijvingen']))),
    leerlingengroepen_vaste_ul = ('leerlingengroep', lambda x: dict(zip(x, df.loc[x.index, 'vaste_ul']))),
    aantal_inschrijvingen=('aantal_inschrijvingen', 'sum'),
    vaste_ul=('vaste_ul', 'sum')
).reset_index()



with pd.ExcelWriter(f'output/jaren/{sys.argv[1]}/1_inschrijvingen_vestigingen.xlsx') as writer:
    df.to_excel(writer, sheet_name='Leerlingengroepen met VUL', index=False)
    df_vul_stdr.to_excel(writer, sheet_name='Studierichtingen met VUL', index=False)
    df_laaste_jaar.to_excel(writer, sheet_name='Laatste Jaar', index=False)