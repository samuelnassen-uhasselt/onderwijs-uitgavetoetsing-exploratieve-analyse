import pandas as pd

ul_tabel = pd.read_excel('uren-leraar-structuuronderdelen.xlsx', sheet_name='NA MODERNISERING').set_index(
    ['structuuronderdeel', 'Graad', 'Onderwijsvorm']).sort_index()
ul_tabel_voor = pd.read_excel('uren-leraar-structuuronderdelen.xlsx', sheet_name='VOOR MODERNISERING').set_index(
    ['structuuronderdeel', 'Onderwijsvorm']).sort_index()

stdr_mapping = {
    'Toerisme (': 'Toerisme',
    'Grafische technieken (': 'Grafische technieken',
    'Grafimedia (': 'Grafimedia',
    'Crossmedia (': 'Crossmedia',
    'Biotechnologische wetenschappen (': 'Biotechnologische wetenschappen',
    'Biotechnologische en chemische wetenschappen (': 'Biotechnologische en chemische wetenschappen',
    'Applicatie- en databeheer (': 'Applicatie- en databeheer',
    'Creatie en mode (': 'Creatie en mode',
    'Mode (': 'Mode',
    'Flexodrukker duaal (': 'Flexodrukker duaal',
    'Architecturale en beeldende kunsten': 'Architecturale en beeldende vorming',
    'Computergestuurde mechanische produktietechnieken': 'Computergestuurde mechanische productietechnieken',
    'Mecanicien tuin-, park- en bosmachines duaal (': 'Mecanicien tuin-, park- en bosmachines duaal',
    'Omsteller verspaning en monteerder-afregelaar duaal': 'Omsteller verspaning en Monteerder-afregelaar duaal',
    'Rotatiedrukker duaal (': 'Rotatiedrukker duaal'
    }

def get_ul(stdr, llngr, lln):
    for keyword, replacement in stdr_mapping.items():
        if keyword in stdr:
            stdr = replacement


    if llngr == '1e graad A':
        return ul_tabel.loc[('1A', 1, 'n.v.t. (1e graad)'), 'uren-leraar_per_student'].item() * lln
    if llngr == '1e graad B':
        return ul_tabel.loc[('1B', 1, 'n.v.t. (1e graad)'), 'uren-leraar_per_student'].item() * lln
    if 'okan' in llngr:
        return ul_tabel.loc[('Onthaaljaar voor anderstalige nieuwkomers', 'n.v.t. (okan)', 'n.v.t. (okan)'), 'uren-leraar_per_student'].item() * lln
    if llngr == 'hbo':
        return ul_tabel.loc[(stdr, 'n.v.t. (hbo)', 'hbo'), 'uren-leraar_per_student'].item() * lln
    
    # VERONDERSTELLING: 4e graad BSO Verpleegkunde = HBO 
    # (bron: https://onderwijstermen.taalunie.org/term/bso/#:~:text=Er%20bestaat%20in%20het%20bso,de%20driejarige%20opleiding%20voor%20verpleegkundige.)
    if llngr == '4e graad bso' and stdr == 'Verpleegkunde':
        return ul_tabel.loc[('Verpleegkunde HBO', 'n.v.t. (hbo)', 'hbo'), 'uren-leraar_per_student'].item() * lln

    try:
        int(llngr[0])
    except:
        return 0
    
    graad = int(llngr[0])
    onderwijsvorm = llngr[-3:].upper()
    try:
        ul = ul_tabel.loc[(stdr, graad, onderwijsvorm)]
        return ul.iloc[0]['uren-leraar_per_student'] * lln
    except:
        try:
            ul = ul_tabel_voor.loc[(stdr, onderwijsvorm)]
            return ul['uren-leraar_per_student'] * lln
        except:
            return 0
