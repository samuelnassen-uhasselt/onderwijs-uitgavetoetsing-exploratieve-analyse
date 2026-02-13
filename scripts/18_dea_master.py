import pandas as pd
import numpy as np
import ast
import get_data

df_units = pd.read_excel('output/16_jaren_samen.xlsx', sheet_name='Units')
df_bestuur = pd.read_excel('output/16_jaren_samen.xlsx', sheet_name='Bestuur')
df_doorstroom_pg = pd.read_excel('Brondata/Doorstroom/UHasselt_doorstroomSR_dataaanvraag2025.xlsx', sheet_name='Participatiegraad')
df_doorstroom_sr = pd.read_excel('Brondata/Doorstroom/UHasselt_doorstroomSR_dataaanvraag2025.xlsx', sheet_name='Studierendement')
df_sb = pd.read_excel('Brondata/Studiebewijzen/20251112-spending review UHasselt.xlsx', sheet_name='SB')
df_vsv = pd.read_excel('Brondata/Studiebewijzen/20251112-spending review UHasselt.xlsx', sheet_name='VSV')
df_master = pd.read_excel('output/16_jaren_samen.xlsx', sheet_name='Master')
df_master_vp = df_master.copy()
df_master_vp.set_index(['vestigingsplaats', 'jaar'], inplace=True)
df_master_bestuur = (df_master.copy()
                     .astype({'schoolbestuur': str, 'jaar': str})
                     .sort_values(by=['schoolbestuur', 'jaar'])
                     .set_index(['schoolbestuur', 'jaar']))

def get_jaar(jaar_code):
    return f'{int(jaar_code)}-{int(jaar_code) + 1}'

# Doorstroom Participatiegraad
df_doorstroom_pg = df_doorstroom_pg[df_doorstroom_pg['Onderwijsvorm code'].isin(['ASO'])]
df_doorstroom_pg['vp_code'] = df_doorstroom_pg['Instellingscode instelling']*100 + df_doorstroom_pg['Intern volgnummer vestigingsplaats']
df_doorstroom_pg['jaar'] = df_doorstroom_pg['Schooljaar code'].apply(get_jaar)
df_doorstroom_pg.set_index(['vp_code', 'jaar'], inplace=True)
df_doorstroom_pg = df_doorstroom_pg.sort_index()

# Doorstroom Studierendement
df_doorstroom_sr = df_doorstroom_sr[df_doorstroom_sr['Onderwijsvorm code'].isin(['ASO'])]
df_doorstroom_sr['vp_code'] = df_doorstroom_sr['Instellingscode instelling']*100 + df_doorstroom_sr['Intern volgnummer vestigingsplaats']
df_doorstroom_sr['jaar'] = df_doorstroom_sr['Code schooljaar afstuderen SO'].apply(get_jaar)
df_doorstroom_sr.set_index(['vp_code', 'jaar'], inplace=True)
df_doorstroom_sr = df_doorstroom_sr.sort_index()

# Studiebewijzen
df_sb['vp_code'] = df_sb['Instellingscode instelling']*100 + df_sb['Intern volgnummer vestigingsplaats']
df_sb['jaar'] = df_sb['Schooljaar code'].apply(get_jaar)
df_sb.set_index(['vp_code', 'jaar'], inplace=True)
df_sb = df_sb.sort_index()

# Vroegtijdig Schoolverlaters
df_vsv['vp_code'] = df_vsv['Instellingscode instelling op moment VSV']*100 + df_vsv['Intern volgnummer vestigingsplaats op moment VSV']
df_vsv['jaar'] = df_vsv['Schooljaar VSV'].apply(get_jaar)
df_vsv.set_index(['vp_code', 'jaar'], inplace=True)
df_vsv = df_vsv.sort_index()

def get_finaliteit(llngroepen):
    aso = False
    tso = False
    bso = False
    kso = False

    for key in ast.literal_eval(llngroepen).keys():
        if 'aso' in key:
            aso = True
        if 'tso' in key:
            tso = True
        if 'bso' in key:
            bso = True
        if 'kso' in key:
            kso = True

    if aso and not tso and not kso and not bso:
        return 'Volledig aso'
    if aso and (tso or kso) and not bso:
        return 'Dubbele doorstroom'
    if aso and (tso or kso) and bso:
        return 'Alle finaliteiten'
    return f'aso:{aso},tso:{tso},bso:{bso}'

def get_dataframe_met_info(df, vp_codes_kolom):
    df[['loopbanen_HO', 'rechtstreeks_HO', 'niet_rechtstreeks_HO', 'niet_HO']] = df.apply(
        lambda row: get_data.get_som_kolommen(
            row[vp_codes_kolom], 
            row['jaar'],
            ['Aantal loopbanen HO','Aantal wel rechtstreeks doorgestroomd naar HO',
            'Aantal niet rechtstreeks doorgestroomd naar HO', 'Aantal niet doorgestroomd naar HO'],
            df_doorstroom_pg
            ), axis=1)
    
    df[['aantal_studietrajecten', 'opgenomen_studiepunten', 'verworven_studiepunten']] = df.apply(
        lambda row: get_data.get_som_kolommen(
            row[vp_codes_kolom], 
            row['jaar'],
            ['Aantal studietrajecten','Opgenomen studiepunten als generatiestudent volgens de instelling',
            'Verworven studiepunten als generatiestudent'],
            df_doorstroom_sr
            ), axis=1)
    df['studierendement'] = df['verworven_studiepunten']/df['opgenomen_studiepunten']

    df[['aantal_studiebewijzen', 'aantal_diploma\'s', 'aantal_getuigschriften']] = df.apply(
        lambda row: get_data.get_som_kolommen(
            row[vp_codes_kolom], 
            row['jaar'],
            ['Aantal studiebewijzen', 'Aantal diploma\'s', 'Aantal studiegetuigschriften'],
            df_sb
        ), axis=1)

    df['gemiddelde_oki'] = df.apply(
        lambda row: get_data.get_oki(
            row[vp_codes_kolom], 
            row['jaar'],
            laatste=False
        ), axis=1)
    
    df['gemiddelde_oki_laatste'] = df.apply(
        lambda row: get_data.get_oki(
            row[vp_codes_kolom], 
            row['jaar'],
            laatste=True
        ), axis=1)

    df[['vsv_teller', 'vsv_noemer']] = df.apply(
        lambda row: get_data.get_som_kolommen(
            row[vp_codes_kolom], 
            row['jaar'],
            ['Teller VSV', 'Noemer VSV'],
            df_vsv
        ), axis=1)
    df['vsv_percent'] = 100*(df['vsv_teller']/df['vsv_noemer'])

    df = df.rename(
        columns={
            'jaar': 'jaar_afgestudeerd_so',
            'llng_tobe': 'leerlingengroepen',
        }
    )
    
    return df

df_units['uren-leraar_asis'] = df_units['ul_vast'] + df_units['ul_asis']
df_units['uren-leraar_tobe'] = df_units['ul_vast'] + df_units['ul_tobe']
df_units['finaliteit'] = df_units['llng_tobe'].apply(get_finaliteit)
df_units = df_units[['unit_code_so', 'jaar', 'schoolbestuur', 'net', 'llng_tobe', 'finaliteit', 
                    'aantal_leerlingen', 'uren-leraar_asis', 'directeurs_asis', 'uren-leraar_tobe',
                    'leerlingen_laatste_jaar', 'vaste_uren-leraar_laatste_jaar', 'deg_uren-leraar_laatste_jaar_asis',
                    'deg_uren-leraar_laatste_jaar_tobe', 'directeurs_laatste_jaar',
                    'leerlingen_laatste_jaar_aso', 'vaste_uren-leraar_laatste_jaar_aso', 'deg_uren-leraar_laatste_jaar_aso_asis',
                    'deg_uren-leraar_laatste_jaar_aso_tobe', 'directeurs_laatste_jaar_aso']]
df_units = get_dataframe_met_info(df_units, 'unit_code_so')

def get_vps_bestuur(bestuur, jaar):
    try:
        df_vps = df_master_bestuur.loc[(bestuur, jaar)]['vestigingsplaats'].dropna()
        return '_'.join(df_vps.astype(str).values)
    except:
        return

df_bestuur['vps'] = df_bestuur.apply(lambda row: get_vps_bestuur(row['schoolbestuur'], row['jaar']), axis=1)
df_bestuur = get_dataframe_met_info(df_bestuur, 'vps')

with pd.ExcelWriter('output/18_dea_master.xlsx') as writer:
    df_units.to_excel(writer, sheet_name='Units', index=False)
    df_bestuur.to_excel(writer, sheet_name='Bestuur', index=False)