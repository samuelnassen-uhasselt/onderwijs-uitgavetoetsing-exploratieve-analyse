import pandas as pd

df = pd.read_excel('output/jaren/2024-2025/4_schoolnummers_llngroepen_ul_inschrijvingen.xlsx')

lln = df['aantal_inschrijvingen'].sum()
dir = df['directeurs'].sum()
kost_oud = 93986 * dir

kost_punt = 782.9
dir_punten = 120
kost_dir = kost_punt * dir_punten

dir_nieuw = kost_oud/kost_dir
lln_per_dir = lln/dir_nieuw
print(dir, dir_nieuw, lln_per_dir)

kost_nieuw = 114000*kost_punt
print(kost_oud, kost_nieuw)