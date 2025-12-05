import pandas as pd
import numpy as np

df_units = pd.read_excel('16d_units_jaren.xlsx')
df_doorstroom_pg = pd.read_excel('Brondata/UHasselt_doorstroomSR_dataaanvraag2025.xlsx', sheet_name='Participatiegraad')
df_doorstroom_sr = pd.read_excel('Brondata/UHasselt_doorstroomSR_dataaanvraag2025.xlsx', sheet_name='Studierendement')

df_doorstroom_pg['jaar'] = df_doorstroom_pg['Schooljaar code'].astype(str) + '-' + (df_doorstroom_pg['Schooljaar code'] + 1).astype(str)
df_doorstroom_pg['vp_code'] = df_doorstroom_pg['Instellingscode instelling']*100 + df_doorstroom_pg['Intern volgnummer vestigingsplaats']
df_doorstroom_pg.set_index(['vp_code', 'jaar'], inplace=True)
df_doorstroom_pg = df_doorstroom_pg.sort_index()

df_doorstroom_sr['jaar'] = df_doorstroom_sr['Code schooljaar afstuderen SO'].astype(str) + '-' + (df_doorstroom_sr['Code schooljaar afstuderen SO'] + 1).astype(str)
df_doorstroom_sr['vp_code'] = df_doorstroom_sr['Instellingscode instelling']*100 + df_doorstroom_sr['Intern volgnummer vestigingsplaats']
df_doorstroom_sr.set_index(['vp_code', 'jaar'], inplace=True)
df_doorstroom_sr = df_doorstroom_sr.sort_index()


def get_sr(vps, jaar):
    vps = vps.replace('SO_', '')
    result = [0, 0, 0]
    columns = [
        'Aantal studietrajecten',
        'Opgenomen studiepunten als generatiestudent volgens de instelling',
        'Verworven studiepunten als generatiestudent'
    ]

    for vp in vps.split('_'):
        try:
            sr = df_doorstroom_sr.loc[(int(vp), jaar)]
            for i, col in enumerate(columns):
                result[i] += np.sum(sr[col])

        except:
            continue
    return pd.Series(result)


df_units['uren-leraar_asis'] = df_units['ul_vast'] + df_units['ul_asis']
df_units[['aantal_studietrajecten', 'opgenomen_studiepunten', 'verworven_studiepunten']] = df_units.apply(lambda row: get_sr(row['unit_code_so'], row['jaar']), axis=1)
df_units['studierendement'] = df_units['verworven_studiepunten']/df_units['opgenomen_studiepunten']
df_units = df_units[['unit_code_so', 'jaar', 'unit_code_SO_actief', 'schoolbestuur', 'net', 'llng_tobe', 
                    'aantal_leerlingen', 'uren-leraar_asis', 'directeurs_asis', 
                    'aantal_studietrajecten', 'opgenomen_studiepunten', 'verworven_studiepunten', 'studierendement']]
df_units = df_units.rename(
    columns={
        'jaar': 'jaar_afgestudeerd_so',
        'llng_tobe': 'leerlingengroepen',
    }
)

df_units.to_excel('18_units_asis_doorstroom.xlsx', index=False)