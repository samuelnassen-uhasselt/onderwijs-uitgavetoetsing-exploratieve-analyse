import pandas as pd
import sys

schooljaar = sys.argv[1]

df_werkingsmiddelen = pd.read_excel('Brondata\\Omkadering\\WT_HS311_2017_2024.xlsx')
jaar = int(schooljaar.split('-')[0])
df_werkingsmiddelen = df_werkingsmiddelen[df_werkingsmiddelen['schooljaar'] == jaar]
df_werkingsmiddelen.set_index('instellingsnummer', inplace=True)

def get_jaar(jaar_code):
    return f'{int(jaar_code)}-{int(jaar_code) + 1}'

def get_sg_naam(naam, provincie):
    if pd.notna(naam):
        result = naam.replace('SGKSO', 'Scholengemeenschap voor katholiek secundair onderwijs')
        result = result.replace('SG', 'Scholengemeenschap')

        if result == 'Scholengemeenschap voor katholiek secundair onderwijs Sint-Michiel':
            if not pd.notna(provincie):
                provincie = 'Limburg'
            result = f'{result} {provincie}'

        return result

df_omkadering = pd.read_excel('Brondata\\Omkadering\\UHasselt_omkadering_2016_2025.xlsx')

df_omkadering['aanwendbare_eenheden'] = df_omkadering['aantal_eenheden'] * df_omkadering['aanwendingspct']/100
df_omkadering['jaar'] = df_omkadering['schooljaar'].apply(get_jaar)
df_omkadering = df_omkadering[df_omkadering['jaar'] == schooljaar]
df_omkadering = df_omkadering.groupby(['school', 'ko_srt_omkadering', 'ko_eenheid'])['aanwendbare_eenheden'].max().reset_index()

df_omkadering = df_omkadering.pivot_table(
    index='school',
    columns='ko_srt_omkadering',
    values='aanwendbare_eenheden',
    aggfunc='sum',
    fill_value=0
)

df_omkadering_gpe = pd.read_excel('Brondata\\Omkadering\\omkadering_generiek_2019-2026.xlsx')
df_omkadering_gpe = df_omkadering_gpe[df_omkadering_gpe['SCHOOLJAAR'] == schooljaar]
df_omkadering_gpe = df_omkadering_gpe[df_omkadering_gpe['NAAM_OMKADERING'] == 'Globale puntenenveloppe']
df_omkadering_gpe['scholengemeenschap'] = df_omkadering_gpe.apply(
    lambda row: get_sg_naam(row['NAAM_INSTELLING'], row['NAAM_PROVINCIE_INSTELLING']), axis=1)
df_omkadering_gpe.set_index('scholengemeenschap', inplace=True)

def get_werkingsmiddelen(row, laatste):
    inschr_inst = row['aantal_inschrijvingen_inst']
    if laatste:
        inschr_part = row['lln_laatste_jaar']
    else:
        inschr_part = row['aantal_inschrijvingen_vp']

    try:
        bedrag = df_werkingsmiddelen['uitbetaald bedrag'].loc[row['schoolnummer']]
        return (inschr_part * bedrag/inschr_inst)
    except:
        return 0

def get_extra_omkadering(row, laatste):
    inschr_inst = row['aantal_inschrijvingen_inst']
    if laatste:
        inschr_part = row['lln_laatste_jaar']
    else:
        inschr_part = row['aantal_inschrijvingen_vp']
    
    try:
        verhouding = inschr_part/inschr_inst
    except:
        return pd.Series([0]*10)

    inschr_sg = row['aantal_inschrijvingen_sg']
    try:
        verhouding_sg = inschr_part/inschr_sg
    except:
        verhouding_sg = 0

    try:
        omk = df_omkadering.loc[row['schoolnummer']]
    except:
        return pd.Series([0]*10)

    ul_cols = ['Aanvangsbegeleiding SO', 'Extra uren-leraar vervolgcoach', 'Extra uren-leraar duaal', 
              'Hertelling uren-leraar capaciteit', 'Ondersteuning kerntaak SO', 'TOAH SO', 
              'TOAH voor jongeren in een voorziening', 'Uren CB teldag', 'Uren ECR teldag', 'Uren GD ANG teldag', 
              'Uren GD ISL teldag', 'Uren GD ISR teldag', 'Uren GD ORT teldag', 'Uren GD PRO teldag', 
              'Uren GD RK teldag', 'Uren GOK 1', 'Uren GOK 23', 'Uren GZ ANG teldag', 'Uren GZ ISL teldag',
              'Uren GZ ISR teldag', 'Uren GZ ORT teldag', 'Uren GZ PRO teldag', 'Uren GZ RK teldag',
              'Uren NCZ teldag', 'Uren OKAN SO', 'Uren school niet in SG', 'Uren topsport',
              'Uren-leraar CB', 'Uren-leraar GD ANG', 'Uren-leraar GD ISL', 'Uren-leraar GD ISR',
              'Uren-leraar GD ORT', 'Uren-leraar GD PRO', 'Uren-leraar GD RK', 'Uren-leraar GOK 1',
              'Uren-leraar GOK 23', 'Uren-leraar NCZ', 'Uren-leraar OKAN SO', 'Uren-leraar afstemming topsport SO',
              'Uren-leraar bijsprong SO', 'Uren-leraar land- en tuinbouw', 'Uren-leraar n.a.v. toename vluchtelingen',
              'Uren-leraar school niet in SG', 'Uren-leraar topsport']
    
    punten_cols = ['ICT-punten', 'Punten ICT', 'Glob Ptn-enveloppe niet in SG']
    
    # TODO: FORFAITAIR / MINIMUM
    
    ul = verhouding*omk.reindex(ul_cols, fill_value=0).sum()

    try:
        forfait = verhouding*omk['Forfaitair pakket']
    except:
        forfait = 0
    try:
        min_paket = verhouding*omk['Minimumpakket']
    except:
        min_paket = 0

    punten = verhouding*omk.reindex(punten_cols, fill_value=0).sum()

    try:
        gpe_punten = verhouding_sg*df_omkadering_gpe.loc[row['scholengemeenschap'], 'TOEGEKENDE_EENHEDEN']
    except:
        gpe_punten = 0

    ambten_cols = ['Adjunct-directeur', 'TA organiek', 'TAC bonusambt', 'TAC organiek',
                  'Teeltleider', 'Topsportschoolcoördinator']
    ambten = {}
    for a in ambten_cols:
        try:
            ambten[a] = verhouding*omk[a]
        except:
            ambten[a] = 0

    return pd.Series([ul, forfait, min_paket, punten+gpe_punten,
                      ambten['Adjunct-directeur'], ambten['TA organiek'], ambten['TAC bonusambt'],
                      ambten['TAC organiek'], ambten['Teeltleider'], ambten['Topsportschoolcoördinator']])

df = pd.read_excel(f'output/jaren/{schooljaar}/5_master_ul_dir.xlsx')

df['scholengemeenschap'] = df.apply(
    lambda row: get_sg_naam(row['scholengemeenschap'], row['provincie']), axis=1)
df_sg = df.groupby('scholengemeenschap')['aantal_inschrijvingen_vp'].sum().reset_index(name='aantal_inschrijvingen_sg')
df = pd.merge(df, df_sg, on='scholengemeenschap', how='left')

df['werkingsmiddelen_vp'] = df.apply(lambda row: get_werkingsmiddelen(row, False), axis=1)
df['werkingsmiddelen_vp_laatste'] = df.apply(lambda row: get_werkingsmiddelen(row, True), axis=1)

df[['extra_ul_aanwendbaar', 'forfaitair_pakket', 'minimumpakket', 'extra_punten_aanwendbaar', 'Adjunct-directeur', 
    'TA organiek', 'TAC bonusambt', 'TAC organiek', 'Teeltleider', 'Topsportschoolcoördinator']] = df.apply(
    lambda row: get_extra_omkadering(row, False), axis=1)
df[['extra_ul_aanwendbaar_laatste', 'forfaitair_pakket_laatste', 'minimumpakket_laatste', 
    'extra_punten_aanwendbaar_laatste', 'Adjunct-directeur_laatste', 'TA organiek_laatste', 'TAC bonusambt_laatste', 
    'TAC organiek_laatste', 'Teeltleider_laatste', 'Topsportschoolcoördinator_laatste']] = df.apply(
    lambda row: get_extra_omkadering(row, True), axis=1)

df = df[['vestigingsplaats', 'schoolnummer',
        'aantal_inschrijvingen_inst', 'aantal_inschrijvingen_vp', 'lln_laatste_jaar',
        'werkingsmiddelen_vp', 'werkingsmiddelen_vp_laatste',
        'extra_ul_aanwendbaar', 'forfaitair_pakket', 'minimumpakket', 'extra_punten_aanwendbaar', 'Adjunct-directeur', 
        'TA organiek', 'TAC bonusambt', 'TAC organiek', 'Teeltleider', 'Topsportschoolcoördinator',
        'extra_ul_aanwendbaar_laatste', 'forfaitair_pakket_laatste', 'minimumpakket_laatste', 
        'extra_punten_aanwendbaar_laatste', 'Adjunct-directeur_laatste', 'TA organiek_laatste', 'TAC bonusambt_laatste', 
        'TAC organiek_laatste', 'Teeltleider_laatste', 'Topsportschoolcoördinator_laatste'
    ]]

df.to_excel(f'output/jaren/{schooljaar}/23_extra_omk_aanwendbaar.xlsx', index=False)