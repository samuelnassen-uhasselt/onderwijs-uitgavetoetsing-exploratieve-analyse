# How to

Om de analyse opnieuw te maken, run het script 'run_scripts.py'.

Hiervoor is de Brondata nodig. Voeg de volgende mappen toe in de brondata:
- Doorstroom
- Inschrijvingen
- OKI
- Omkadering
- Studiebewijzen
- Units en complexen
- Vestigingsplaatsen

Het script maakt eerst een map 'output' aan met daarin een map 'jaren' waarvoor voor elk jaar beschikbaar in de inschrijvingen alle scripts worden gerund.
Deze jaren worden daarna samengevoegd in grotere bestanden.

NOTA: Er is 1 bestand dat nog wordt aangepast na het aanmaken ervan, namelijk 5_master_ul_dir.xlsx. In 5 master_ul_dir.py wordt het bestand aangemaatk voor de AS-IS berekeningen. Achteraf wordt in 8_analyze_units_llngroepen.py de TO-BE aan dit xlsx bestand toegevoegd.
Alle andere xlsx bestanden worden volledig berekend aan de hand van het overeenstemmende .py bestand.