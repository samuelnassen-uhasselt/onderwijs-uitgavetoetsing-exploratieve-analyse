import subprocess

r_path = "C:\\Program Files\\R\\R-4.5.2\\bin\\Rscript.exe"
script = "C:\\Users\\lucp14223\\Files\\programmeren\\onderwijs\\mergoni_dea.r"

res = subprocess.call([r_path, script])
print(res)