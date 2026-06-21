#From promp: pip install fsspec
import pandas as pd
from collections import Counter


def densita_coppie_finestre(file_path="testFile.txt", dimensione_finestra=100):
    try:
        df = pd.read_csv(file_path, sep='\s+', header=None)
        b = df.iloc[:, 2].tolist()
        c = df.iloc[:, 3].tolist()
        coppie = list(zip(b, c))
        risultati_finestre = []
        for i in range(0, len(coppie), dimensione_finestra):
            finestra = coppie[i:i + dimensione_finestra]
            conteggio_finestra = Counter(finestra)
            risultati_finestre.append(conteggio_finestra)
        return risultati_finestre
    except FileNotFoundError:
        return "Error: File Not Found."

risultati_finestre = densita_coppie_finestre()

if isinstance(risultati_finestre, list):
    print("\nLocal the pair density (b, c) in window:")
    for i, conteggio_finestra in enumerate(risultati_finestre):
        print(f"  Finestra da {i * 100} a {(i + 1) * 100}:")
        for coppia, frequenza in conteggio_finestra.items():
            print(f"  pair {coppia}: {frequenza} frequency ")
else:
    print(risultati_finestre)
