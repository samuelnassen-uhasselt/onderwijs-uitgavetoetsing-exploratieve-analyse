import pandas as pd
import numpy as np
import ast
import requests
import sys

schooljaar = sys.argv[1]

df_laatste_jaar = pd.read_excel(f'output/jaren/{schooljaar}/1_inschrijvingen_vestigingen.xlsx', sheet_name='Laatste Jaar')
df_laatste_jaar.set_index('vestigingsplaats', inplace=True)
df_werkingsmiddelen = pd.read_excel(f'Brondata\\Omkadering\\WT_HS311_2017_2024.xlsx')
jaar = int(schooljaar.split('-')[0])
df_werkingsmiddelen = df_werkingsmiddelen[df_werkingsmiddelen['schooljaar'] == jaar]
df_werkingsmiddelen.set_index('instellingsnummer', inplace=True)


def get_jaar(jaar_code):
    return f'{int(jaar_code)}-{int(jaar_code) + 1}'

df_omkadering = pd.read_excel('Brondata\\Omkadering\\UHasselt_omkadering_2016_2025.xlsx')

df_omkadering['aanwendbare_eenheden'] = df_omkadering['aantal_eenheden'] * df_omkadering['aanwendingspct']/100
df_omkadering['jaar'] = df_omkadering['schooljaar'].apply(get_jaar)
df_omkadering = df_omkadering.groupby([
    'jaar', 'school', 'ko_srt_omkadering', 'ko_eenheid'])['aanwendbare_eenheden'].max().reset_index()

df_omkadering = df_omkadering.pivot_table(
    index=['jaar', 'school'],
    columns='ko_srt_omkadering',
    values='aanwendbare_eenheden',
    aggfunc='sum',
    fill_value=0
)


adres_hernoeming = {
    'Essen, Rouwmoer 7_B':'Essen, Rouwmoer 7B',
    'Genk, Synaps Park 5400_':'Genk, Synaps Park 5400',
    'Bornem, Driesstraat 10':'Kardinaal Cardijnplein 11, 2880 Bornem',
    'Diest, Rozengaard Z/N':'Diest, Rozengaard',
    'Diest, Rozengaard z/n':'Diest, Rozengaard',
    'Haacht, Stationsstraat 91':'Haacht, Stationsstraat 87',
    'Torhout, Spinneschoolstraat 10':'Torhout, Spinneschoolstraat 2',
    'Buggenhout, Collegestraat 5':'Buggenhout, Collegestraat 10',
    'Dendermonde, Noordlaan 51':'Dendermonde, Noordlaan 104',
    'Lokeren, Luikstraat 61':'Lokeren, Luikstraat 65',
    'Essen, Hofstraat 14':'Essen, Hofstraat 12a',
    'Kortrijk, Burgemeester Felix de Bethunelaa 4':'Kortrijk, Burgemeester Felix de Bethunelaan 4',
    'Gent, Coupure Rechts 312':'Coupure 312, 9000 Gent',
    'Tienen, Waaibergstraat 45':'Tienen, Waaibergstraat 93',
    'Tienen, Waaibergstraat 43':'Tienen, Waaibergstraat 5',
    'Antwerpen, Willem Gijsselsstraat 22':'Antwerpen, Willem Gijsselsstraat 15',
    'Antwerpen, Van Helmontstraat 27':'Antwerpen, Pothoekstraat 125',
    'Ardooie, Gapaardstraat 34':'Ardooie, Gapaardstraat 28',
    'Sint-Katelijne-Waver, Borgersteinlei 203':'Sint-Katelijne-Waver, Borgersteinlei 201',
    'Gent, Spitaalpoortstraat 50':'Gent, Spitaalpoortstraat 58',
    'Essen, Rouwmoer 7 B':'Essen, Rouwmoer 7B',
    'Antwerpen, Willem Gijsselsstraat 20':'Antwerpen, Willem Gijsselsstraat 2',
    'Gent, Neermeerskaai 1 A':'Gent, Neermeerskaai 1A',
    'Berlaar, Sollevelden 3 A':'Berlaar, Sollevelden 3A',
    'Ichtegem, Aartrijkestraat 12 A':'Ichtegem, Aartrijkestraat 12A',
    'Pelt, Dorpsstraat 91':'Schrijnwerkerijstraat 1, 3900 Pelt',
    'Genk, Schiepse Bos campus LiZa 5':'Synaps Park 5400A, 3600 Genk',
    'Vilvoorde, Zennelaan 51_53':'Zennelaan 51, 1800 Vilvoorde',
    'Bredene, Unescostraat Z/N':'Unescostraat 1, 8450 Bredene',
    'Gent, Neermeerskaai 1_':'Gent, Neermeerskaai 1',
    'Berlaar, Sollevelden 3_A':'Berlaar, Sollevelden 3A',
    'Ichtegem, Aartrijkestraat 12_A':'Ichtegem, Aartrijkestraat 12A',
    'Heist-op-den-Berg, Leuvensebaan 25-27':'Heist-op-den-Berg, Leuvensebaan 25',
    'Oostende, Leon Spilliaertstraat 30':'Leon Spilliaertstraat 28, 8400 Oostende',
    'Tessenderlo-Ham, Kerkstraat 4_A':'Tessenderlo-Ham, Kerkstraat 4A',
    'Pelt, Ursulinenstraat 13_17':'Pelt, Ursulinenstraat 17',
    'Antwerpen, Lange Nieuwstraat 94':'Lange Nieuwstraat 90, 2000 Antwerpen',
    'Machelen, Cornelis Peetersstraat 39':'Corneille Peetersstraat 35, 1830 Machelen',
    'Wevelgem, Caesar Gezellestraat 7':'Caesar Gezellestraat 9, 8560 Wevelgem',
    'Merelbeke-Melle, Beekstraat 38':'Beekstraat 40, 9090 Merelbeke‑Melle',
    'Ieper, Minneplein Z/N':'Plumerlaan 24, 8900 Ieper',
    'Houthalen-Helchteren, Lyceumstraat 11':'Houthalen-Helchteren, Lyceumstraat 9',
    'Oudsbergen, Kloosterstraat 11':'Kloosterstraat 9, 3670 Oudsbergen',
    'Kortrijk, Boerderijstraat 69_A':'Kortrijk, Boerderijstraat 69',
    'Tervuren, Brusselsesteenweg 106':'Vanderhaegenhof 2B, 3080 Tervuren',
    'Beringen, Burgemeester Geyskensstraat 11':'Burgemeester Geyskensstraat 8, 3580 Beringen',
    'Brugge, Hugo Losschaertstraat 5_A':'Brugge, Hugo Losschaertstraat 5A',
    'Antwerpen, Stoomstraat 11':'Mediaplein 3, 2018 Antwerpen',
    'Kortrijk, Langemeersstraat 3':'Langemeersstraat 15, 8500 Kortrijk',
    'Dilsen-Stokkem, Stadsgraaf Campus Dilsen-Stokkem 22': 'Schuttersstraat 7, 3650 Dilsen‑Stokkem',
    'Wingene, Pensionaatstraat 10': 'Wingene, Pensionaatstraat 8',
    'Lokeren, H.-Hartlaan 1_A': 'Lokeren, H.-Hartlaan 1A'
}

def get_uren_leraar(llngr_vp, llngr_inst):
    if pd.notna(llngr_vp):
        vp_dict = ast.literal_eval(llngr_vp)
        inst_dict = ast.literal_eval(llngr_inst)
        result = {}
        for key, value in vp_dict.items():
            ul = inst_dict[key]['uren-leraar']*(value/inst_dict[key]['inschrijvingen'])
            result[key] = {
                'inschrijvingen': value,
                'ul': ul,
            }
        return result
    
def ul_vp(llngroepen):
    if pd.notna(llngroepen):
        result = 0
        for key, value in llngroepen.items():
            result += value['ul']
        return result

def lln_laatste_jaar(vp, aso):
    try:
        llngr = df_laatste_jaar.loc[[vp]]
        if aso:
            llngr = llngr[llngr['leerlingengroep'].isin(['3e graad aso'])]
        return np.sum(llngr['aantal_inschrijvingen'])
    except:
        return 0

def ul_laatste_jaar(vp, ul_llngr, aso):
    result = {}
    vast = 0
    deg = 0
    try:
        llngr_lj = df_laatste_jaar.loc[[vp]]
        if aso:
            llngr_lj = llngr_lj[llngr_lj['leerlingengroep'].isin(['3e graad aso'])]
    except:
        if not aso:
            return pd.Series([result, vast, deg])
        return pd.Series([vast, deg])
    llngr_lj = llngr_lj.to_dict('records')
    for llngr in llngr_lj:
        tot_lln = ul_llngr[llngr['leerlingengroep']]['inschrijvingen']
        lln_lj = llngr['aantal_inschrijvingen']
        vast += llngr['vaste_ul']
        ul_deg_vp = ul_llngr[llngr['leerlingengroep']]['ul']
        deg += lln_lj*ul_deg_vp/tot_lln
        if llngr['leerlingengroep'] not in result.keys():
            result[llngr['leerlingengroep']] = 0
        result[llngr['leerlingengroep']] += lln_lj
    if not aso:
        return pd.Series([result, vast, deg])
    return pd.Series([vast, deg])

def get_coords(adres):
    # Adressen die de api niet kan vinden
    if adres in adres_hernoeming.keys():
        adres = adres_hernoeming[adres]

    url = 'https://geo.api.vlaanderen.be/geolocation/v4/Location'

    params = {
        'q': adres,
        'c': 1
    }

    response = requests.get(url,params=params).json()

    location = response['LocationResult'][0]['Location']
    lx = int(round(location['X_Lambert72'], 0))
    ly = int(round(location['Y_Lambert72'], 0))
    return lx, ly

def get_lambert(row):
    lx = row['lx']
    ly = row['ly']
    if not pd.notna(lx):
        adres = row['vestigingsplaats_adres']
        if pd.notna(adres):
            return pd.Series(get_coords(adres))
    return pd.Series([lx, ly])

def get_werkingsmiddelen(row, laatste, aso):
    inschr_inst = row['aantal_inschrijvingen_inst']
    if laatste:
        if aso:
            inschr_part = row['lln_laatste_jaar_aso']
        else:
            inschr_part = row['lln_laatste_jaar']
    else:
        inschr_part = row['aantal_inschrijvingen_vp']

    try:
        bedrag = df_werkingsmiddelen['uitbetaald bedrag'].loc[row['schoolnummer']]
        return (inschr_part * bedrag/inschr_inst)
    except:
        return 0

def get_extra_omkadering(row, laatste, aso):
    inschr_inst = row['aantal_inschrijvingen_inst']
    if laatste:
        if aso:
            inschr_part = row['lln_laatste_jaar_aso']
        else:
            inschr_part = row['lln_laatste_jaar']
    else:
        inschr_part = row['aantal_inschrijvingen_vp']
    
    try:
        verhouding = inschr_part/inschr_inst
    except:
        return pd.Series([0,0,0])

    try:
        omk = df_omkadering.loc[(schooljaar, row['schoolnummer'])]
    except:
        return pd.Series([0,0,0])
    
    # TODO: FORFAITAIR / MINIMUM

    ul = omk[['Aanvangsbegeleiding SO', 'Extra uren-leraar vervolgcoach', 'Extra uren-leraar duaal', 
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
              'Uren-leraar school niet in SG', 'Uren-leraar topsport']].sum()
    ambten = omk[['Adjunct-directeur', 'TA organiek', 'TAC bonusambt', 'TAC organiek',
                  'Teeltleider', 'Topsportschoolcoördinator']].sum()
    punten = omk[['ICT-punten', 'Punten ICT', 'Glob Ptn-enveloppe niet in SG']].sum()

    return pd.Series([verhouding*ul, verhouding*ambten, verhouding*punten])


df_master = pd.read_excel(f'output/jaren/{sys.argv[1]}/3_vestigingsplaatsen_master.xlsx')
df_schoolnummers = pd.read_excel(f'output/jaren/{sys.argv[1]}/4_schoolnummers_llngroepen_ul_inschrijvingen.xlsx')

# Merge met scholen getallen om procentuele berekeningen te kunnen doen
df = pd.merge(df_master, df_schoolnummers, how='left', on='schoolnummer', suffixes=['_vp', '_inst'])

# Vul missend lx en ly in
df[['lx', 'ly']] = df.apply(get_lambert, axis=1)

# Bereken de percentages
df['directeur_vp'] = df['aantal_inschrijvingen_vp']*df['directeurs']/df['aantal_inschrijvingen_inst']
df['ul_llngroepen'] = df.apply(lambda row: get_uren_leraar(
    row['leerlingengroepen_vp'], row['leerlingengroepen_inst']), axis=1)
df['ul_vp'] = df['ul_llngroepen'].apply(ul_vp)
df['lln_laatste_jaar'] = df.apply(lambda row: lln_laatste_jaar(row['vestigingsplaats'], False), axis=1)
df[['llngroepen_laatste_jaar', 'ul_vast_vp_laatste_jaar', 'ul_deg_asis_vp_laatste_jaar']] = df.apply(
    lambda row: ul_laatste_jaar(row['vestigingsplaats'], row['ul_llngroepen'], False), axis=1)
df['dir_laatste_jaar'] = df['directeur_vp'] * df['lln_laatste_jaar']/df['aantal_inschrijvingen_vp']
df['lln_laatste_jaar_aso'] = df.apply(lambda row: lln_laatste_jaar(row['vestigingsplaats'], True), axis=1)
df[['ul_vast_vp_laatste_jaar_aso', 'ul_deg_asis_vp_laatste_jaar_aso']] = df.apply(lambda row: ul_laatste_jaar(
    row['vestigingsplaats'], row['ul_llngroepen'], True), axis=1)
df['dir_laatste_jaar_aso'] = df['directeur_vp'] * df['lln_laatste_jaar_aso']/df['aantal_inschrijvingen_vp']
df['lln_per_dir'] = df['aantal_inschrijvingen_vp']/df['directeur_vp']
df['ul_per_lln'] = (df['vaste_ul_vp'] + df['ul_vp'])/df['aantal_inschrijvingen_vp']

df['werkingsmiddelen_vp'] = df.apply(lambda row: get_werkingsmiddelen(row, False, False), axis=1)
df['werkingsmiddelen_vp_laatste'] = df.apply(lambda row: get_werkingsmiddelen(row, True, False), axis=1)
df['werkingsmiddelen_vp_laatste_aso'] = df.apply(lambda row: get_werkingsmiddelen(row, True, True), axis=1)

df[['extra_ul_aanwendbaar', 'extra_ambten_aanwendbaar', 'extra_punten_aanwendbaar']] = df.apply(
    lambda row: get_extra_omkadering(row, False, False), axis=1)
df[['extra_ul_aanwendbaar_laatste', 'extra_ambten_aanwendbaar_laatste', 'extra_punten_aanwendbaar_laatste']] = df.apply(
    lambda row: get_extra_omkadering(row, True, False), axis=1)
df[['extra_ul_aanwendbaar_laatste_aso', 'extra_ambten_aanwendbaar_laatste_aso', 'extra_punten_aanwendbaar_laatste_aso']] = df.apply(
    lambda row: get_extra_omkadering(row, True, True), axis=1)

df.to_excel(f'output/jaren/{schooljaar}/5_master_ul_dir.xlsx', index=False)