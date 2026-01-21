import math

degressieve_ul = {
    '1e graad A': {
        'lln': [25, 50, 100],
        'coef': [0.65, 0.35, 0.2]
    },
    '1e graad B': {
        'lln': [25, 50, 100],
        'coef': [0.6, 0.3, 0.15]
    },
    'n.v.t. (okan) n.v.t. (okan)': {
        'lln': [25, 50, 100],
        'coef': [0.65, 0.35, 0.2]
    },
    '2e graad aso': {
        'lln': [25, 50, 100],
        'coef': [0.45, 0.25, 0.15]
    },
    '2e graad tso': {
        'lln': [25, 75, 150],
        'coef': [0.5, 0.3, 0.1]
    },
    '2e graad bso': {
        'lln': [25, 75, 150],
        'coef': [0.6, 0.3, 0.15]
    },
    '3e graad aso': {
        'lln': [25, 50, 100],
        'coef': [0.45, 0.25, 0.15]
    },
    '3e graad tso': {
        'lln': [25, 75, 150],
        'coef': [0.5, 0.3, 0.1, ]
    },
    '3e graad bso': {
        'lln': [25, 75, 150],
        'coef': [0.6, 0.3, 0.15]
    },
}

degressieve_ul_herwerkt = {
    '1e graad A': {
        'lln': [25, 50, 100],
        'coef': [0.65, 0.35, 0.2]
    },
    '1e graad B': {
        'lln': [25, 50, 100],
        'coef': [0.6, 0.3, 0.15]
    },
    'n.v.t. (okan) n.v.t. (okan)': {
        'lln': [25, 50, 100],
        'coef': [0.65, 0.35, 0.2]
    },
    '2e graad aso': {
        'lln': [25, 50, 100],
        'coef': [0.45, 0.25, 0.15]
    },
    '2e graad tso': {
        'lln': [25, 75, 150],
        'coef': [0.5, 0.3, 0.1]
    },
    '2e graad bso': {
        'lln': [25, 75, 150],
        'coef': [0.6, 0.3, 0.15]
    },
    '3e graad aso': {
        'lln': [25, 50, 100],
        'coef': [0.45, 0.25, 0.15]
    },
    '3e graad tso': {
        'lln': [25, 75, 150],
        'coef': [0.5, 0.3, 0.1]
    },
    '3e graad bso': {
        'lln': [25, 75, 150],
        'coef': [0.6, 0.3, 0.15]
    },
}

degressieve_ul_herwerkt_alle = {
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
def get_degressieve_uren_leraar(llngroep, aantal, herwerkt, alt):
    if ((llngroep == 'hbo') or (llngroep == 'n.v.t. (modulair) bso') or 
        (llngroep == '2e graad kso') or (llngroep == '3e graad kso') or
        (llngroep == '4e graad bso')):
        return 0
    if llngroep == '1e graad 2':
        llngroep = '1e graad A'
    if llngroep == '1e graad BV':
        llngroep = '1e graad B'

    factor = 0
    coef_alt = 0
    if herwerkt == 'DEEL':
        coef_alt = alt[herwerkt][llngroep]
    elif herwerkt == 'ALLE':
        factor = alt[herwerkt][llngroep]
    lln = degressieve_ul[llngroep]['lln']
    coef = degressieve_ul[llngroep]['coef']

    if aantal > lln[2]:
        return round(lln[0] * coef[0] + (lln[1] - lln[0]) * coef[1] + 
                     (lln[2] - lln[1]) * coef[2] + (aantal - lln[2]) * coef_alt + aantal * factor, 2)
    if aantal > lln[1]:
        return round(lln[0] * coef[0] + (lln[1] - lln[0]) * coef[1] + (aantal - lln[1]) * coef[2] + aantal * factor, 2)
    if aantal > lln[0]: 
        return round(lln[0] * coef[0] + (aantal - lln[0]) * coef[1] + aantal * factor, 2)
    return round(aantal * coef[0] + aantal * factor, 2)
