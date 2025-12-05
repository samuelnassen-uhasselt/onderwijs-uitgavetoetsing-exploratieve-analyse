import pandas as pd
import sys

vestigingen = "Brondata/Vestigingsplaatsen/vestigingsplaatsen-van-scholen-gewoon-secundair-onderwijs_2024-2025.xlsx"

df = pd.read_excel(vestigingen)
df['vestigingsplaats'] = df['schoolnummer'].astype(str) + df['intern_vplnummer'].astype(str).str.zfill(2)

df.to_excel(f'jaren/{sys.argv[1]}/0_vestigingsplaatsen_volledig_nummer.xlsx', index=False)