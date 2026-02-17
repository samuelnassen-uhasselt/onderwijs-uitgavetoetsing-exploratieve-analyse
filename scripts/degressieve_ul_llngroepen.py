degressieve_ul = {
    '1e graad A': {
        'lln': [25, 50, 100],
        'coef': [0.65, 0.35, 0.2, 0]
    },
    '1e graad B': {
        'lln': [25, 50, 100],
        'coef': [0.6, 0.3, 0.15, 0]
    },
    'okan': {
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

ul_herverdeeld = {
        '1e graad A': [0.65, 0.35, 0.2, 0.0855319652665379],
        '1e graad B': [0.6, 0.3, 0.22998499939738037, 0.22998499939738037],
        '2e graad bso': [0.6, 0.3, 0.19723642385250942, 0.19723642385250942],
        '2e graad tso': [0.5, 0.3, 0.12806577487357196, 0.12806577487357196],
        '3e graad bso': [0.6, 0.3, 0.1544549376361994, 0.1544549376361994],
        '3e graad tso': [0.5, 0.3, 0.1142292178183496, 0.1142292178183496],
        '2e graad kso': [0, 0, 0, 0],
        '3e graad kso': [0, 0, 0, 0],
        'okan': [0.65, 0.35, 0.2, 0.0],
        'hbo': [0, 0, 0, 0],
        '2e graad aso': [0.45, 0.25, 0.15, 0.010999865751965522],
        '3e graad aso': [0.45, 0.25, 0.15, 0.014909820336183313],
        'n.v.t. (modulair) bso': [0, 0, 0, 0],
        '4e graad bso': [0, 0, 0, 0],
    }

punten_dir_herverdeeld = 0.249611554599382

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

    if herwerkt:
        coef = alt[llngroep]
    else:
        coef = degressieve_ul[llngroep]['coef']
    lln = degressieve_ul[llngroep]['lln']    

    if aantal > lln[2]:
        return round(lln[0] * coef[0] + (lln[1] - lln[0]) * coef[1] + 
                     (lln[2] - lln[1]) * coef[2] + (aantal - lln[2]) * coef[3], 2)
    if aantal > lln[1]:
        return round(lln[0] * coef[0] + (lln[1] - lln[0]) * coef[1] + (aantal - lln[1]) * coef[2], 2)
    if aantal > lln[0]: 
        return round(lln[0] * coef[0] + (aantal - lln[0]) * coef[1], 2)
    return round(aantal * coef[0], 2)
