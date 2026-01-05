import pandas as pd

df_omkadering = pd.read_excel('Brondata\\Omkadering\\UHasselt_omkadering_2016_2025.xlsx')

def get_jaar(jaar_code):
    return f'{int(jaar_code)}-{int(jaar_code) + 1}'

def get_percent_v_eenheid(aanw, ambten, punten, ul, soort):
    if soort == 'ambten':
        return aanw*100/ambten
    if soort == 'punten':
        return aanw*100/punten
    if soort == 'uren-leraar':
        return aanw*100/ul

df_omkadering['aanwendbare_eenheden'] = df_omkadering['aantal_eenheden'] * df_omkadering['aanwendingspct']/100
df_omkadering['jaar'] = df_omkadering['schooljaar'].apply(get_jaar)
df_omkadering = df_omkadering.groupby([
    'jaar', 'school', 'ko_srt_omkadering', 'ko_eenheid'])['aanwendbare_eenheden'].max().reset_index()

df_pivot_eenheid = df_omkadering.pivot_table(
    index=['jaar', 'school'],
    columns='ko_eenheid',
    values='aanwendbare_eenheden',
    aggfunc='sum',
    fill_value=0
)

df_omkadering = pd.merge(df_omkadering, df_pivot_eenheid, on=['jaar', 'school'], how='left')
df_omkadering['percent_eenheid'] = df_omkadering.apply(lambda row:
                        get_percent_v_eenheid(
                            row['aanwendbare_eenheden'],
                            row['ambten'],
                            row['punten'],
                            row['uren-leraar'],
                            row['ko_eenheid']
                        ),
                        axis=1)

df_pivot_ok = df_omkadering.pivot_table(
    index=['jaar', 'school'],
    columns='ko_srt_omkadering',
    values='percent_eenheid',
    aggfunc='sum',
    fill_value=0
)

df_pivot = pd.merge(df_pivot_ok, df_pivot_eenheid, on=['jaar', 'school'], how='outer').reset_index()

df_pivot.to_excel('test.xlsx', index=False)