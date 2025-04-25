# Funzione per calcolare la densità locale delle coppie in finestre
import pandas as pd
from collections import Counter

def densita_coppie_finestre(file_path="D://Documenti//----Numeri//Codice Python//testFile.txt", dimensione_finestra=100):
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
        return "Errore: File non trovato."

# Calcola e stampa la densità delle coppie per finestre
risultati_finestre = densita_coppie_finestre()

if isinstance(risultati_finestre, list):
    print("\nDensità Locale delle Coppie (b, c) in Finestre:")
    for i, conteggio_finestra in enumerate(risultati_finestre):
        print(f"  Finestra da {i * 100} a {(i + 1) * 100}:")
        for coppia, frequenza in conteggio_finestra.items():
            print(f"    Coppia {coppia}: {frequenza} volte")
else:
    print(risultati_finestre)
