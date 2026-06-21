#From promp: pip install fsspec
import pandas as pd
from collections import Counter

def frequenza_coppie(file_path="testFile.txt"):
    try:
        df = pd.read_csv(file_path, sep='\s+', header=None)
        b = df.iloc[:, 2].tolist()
        c = df.iloc[:, 3].tolist()
        coppie = list(zip(b, c))
        conteggio_coppie = Counter(coppie)
        return conteggio_coppie
    except FileNotFoundError:
        return "Error: File not found."

conteggio_coppie = frequenza_coppie()
if isinstance(conteggio_coppie, Counter):
    print("Frequenza Globale delle Coppie (b, c):")
    for coppia, frequenza in conteggio_coppie.items():
        print(f"  pair {coppia}: {frequenza} frequency ")
else:
    print(conteggio_coppie)
