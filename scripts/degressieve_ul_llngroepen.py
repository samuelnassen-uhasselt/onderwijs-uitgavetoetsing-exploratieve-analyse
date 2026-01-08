import math

degressieve_ul = {
    '1e graad A': {
        'lln': [25, 50, 100],
        'coef': [0.65, 0.35, 0.2, 0]
    },
    '1e graad B': {
        'lln': [25, 50, 100],
        'coef': [0.6, 0.3, 0.15, 0]
    },
    'n.v.t. (okan) n.v.t. (okan)': {
        'lln': [25, 50, 100],
        'coef': [0.65, 0.35, 0.2, 0]
    },
    '2e graad aso': {
        'lln': [25, 50, 100],
        'coef': [0.45, 0.25, 0.15, 0]
    },
    '2e graad tso': {
        'lln': [25, 75, 150],
        'coef': [0.5, 0.3, 0.1, 0]
    },
    '2e graad bso': {
        'lln': [25, 75, 150],
        'coef': [0.6, 0.3, 0.15, 0]
    },
    '3e graad aso': {
        'lln': [25, 50, 100],
        'coef': [0.45, 0.25, 0.15, 0]
    },
    '3e graad tso': {
        'lln': [25, 75, 150],
        'coef': [0.5, 0.3, 0.1, 0]
    },
    '3e graad bso': {
        'lln': [25, 75, 150],
        'coef': [0.6, 0.3, 0.15, 0]
    },
}

degressieve_ul_herwerkt = {
    '1e graad A': {
        'lln': [25, 50, 100],
        'coef': [0.65, 0.35, 0.2, 6673.25/77237]
    },
    '1e graad B': {
        'lln': [25, 50, 100],
        'coef': [0.6, 0.3, 0.15, 1189.2/2772]
    },
    'n.v.t. (okan) n.v.t. (okan)': {
        'lln': [25, 50, 100],
        'coef': [0.65, 0.35, 0.2, -146.8/911]
    },
    '2e graad aso': {
        'lln': [25, 50, 100],
        'coef': [0.45, 0.25, 0.15, 359/32309]
    },
    '2e graad tso': {
        'lln': [25, 75, 150],
        'coef': [0.5, 0.3, 0.1, 1700.1/10232]
    },
    '2e graad bso': {
        'lln': [25, 75, 150],
        'coef': [0.6, 0.3, 0.15, 1210.95/3991]
    },
    '3e graad aso': {
        'lln': [25, 50, 100],
        'coef': [0.45, 0.25, 0.15, 315.65/20958]
    },
    '3e graad tso': {
        'lln': [25, 75, 150],
        'coef': [0.5, 0.3, 0.1, 1775.9/13571]
    },
    '3e graad bso': {
        'lln': [25, 75, 150],
        'coef': [0.6, 0.3, 0.15, 1393.5/8590]
    },
}

degressieve_ul_herwerkt_alle = {
    '1e graad A': {
        'lln': [25, 50, 100],
        'coef': [0.65, 0.35, 0.2, 0],
        'factor': 0.052613632

    },
    '1e graad B': {
        'lln': [25, 50, 100],
        'coef': [0.6, 0.3, 0.15, 0],
        'factor': 0.045911513

    },
    'n.v.t. (okan) n.v.t. (okan)': {
        'lln': [25, 50, 100],
        'coef': [0.65, 0.35, 0.2, 0],
        'factor': -0.018363773
    },
    '2e graad aso': {
        'lln': [25, 50, 100],
        'coef': [0.45, 0.25, 0.15, 0],
        'factor': 0.005479912

    },
    '2e graad tso': {
        'lln': [25, 75, 150],
        'coef': [0.5, 0.3, 0.1, 0],
        'factor': 0.033779729
    },
    '2e graad bso': {
        'lln': [25, 75, 150],
        'coef': [0.6, 0.3, 0.15, 0],
        'factor': 0.03429676
    },
    '3e graad aso': {
        'lln': [25, 50, 100],
        'coef': [0.45, 0.25, 0.15, 0],
        'factor': 0.006126271
    },
    '3e graad tso': {
        'lln': [25, 75, 150],
        'coef': [0.5, 0.3, 0.1, 0],
        'factor': 0.032201853
    },
    '3e graad bso': {
        'lln': [25, 75, 150],
        'coef': [0.6, 0.3, 0.15, 0],
        'factor': 0.031625173
    },
}

# Geen rekening gehouden met:
# - mogelijke veranderingen ten gevolge van de Oekraïne-crisis
# - puntje 3 omtrent scholen met hoofdvestigingsplaats in Brussel of dun-bevolkte gemeenten
# - tellingsdatum
# - Minimum pakketten
# - Bijzonder pakket voor scholen in afbouw
# - Specifieke regelingen (topsport, maritieme scholen, land- en tuinbouwscholen)
# - Levensbeschouwelijke vakken (godstdienst, niet-confessionele zedenleer, cultuurbeschouwing, cultuur en religie)
# - Fusies en opsplitsingen
# - Scholen buiten scholengemeenschappen
# - Bijkomende uren-leraar samen school maken
def get_degressieve_uren_leraar(llngroep, aantal, herwerkt):
    if ((llngroep == 'hbo') or (llngroep == 'n.v.t. (modulair) bso') or 
        (llngroep == '2e graad kso') or (llngroep == '3e graad kso') or
        (llngroep == '4e graad bso')):
        return 0
    if llngroep == '1e graad 2':
        llngroep = '1e graad A'
    if llngroep == '1e graad BV':
        llngroep = '1e graad B'

    if herwerkt == 'DEEL':
        lln = degressieve_ul_herwerkt[llngroep]['lln']
        coef = degressieve_ul_herwerkt[llngroep]['coef']
        factor = 0
    elif herwerkt == 'ALLE':
        lln = degressieve_ul_herwerkt_alle[llngroep]['lln']
        coef = degressieve_ul_herwerkt_alle[llngroep]['coef']
        factor = degressieve_ul_herwerkt_alle[llngroep]['factor']
    else:
        lln = degressieve_ul[llngroep]['lln']
        coef = degressieve_ul[llngroep]['coef']
        factor = 0

    if aantal > lln[2]:
        return round(lln[0] * coef[0] + (lln[1] - lln[0]) * coef[1] + 
                     (lln[2] - lln[1]) * coef[2] + (aantal - lln[2]) * coef[3] + aantal * factor, 2)
    if aantal > lln[1]:
        return round(lln[0] * coef[0] + (lln[1] - lln[0]) * coef[1] + (aantal - lln[1]) * coef[2] + aantal * factor, 2)
    if aantal > lln[0]: 
        return round(lln[0] * coef[0] + (aantal - lln[0]) * coef[1] + aantal * factor, 2)
    return round(aantal * coef[0] + aantal * factor, 2)
