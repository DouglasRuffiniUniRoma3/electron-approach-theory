import pandas as pd
from collections import Counter

# Funzione per calcolare la frequenza delle coppie (b, c)
def frequenza_coppie(file_path="D://Documenti//----Numeri//Codice Python//testFile.txt"):
    try:
        df = pd.read_csv(file_path, sep='\s+', header=None)
        b = df.iloc[:, 2].tolist()
        c = df.iloc[:, 3].tolist()
        coppie = list(zip(b, c))
        conteggio_coppie = Counter(coppie)
        return conteggio_coppie
    except FileNotFoundError:
        return "Errore: File non trovato."

# Calcola e stampa la frequenza delle coppie
conteggio_coppie = frequenza_coppie()

if isinstance(conteggio_coppie, Counter):
    print("Frequenza Globale delle Coppie (b, c):")
    for coppia, frequenza in conteggio_coppie.items():
        print(f"  Coppia {coppia}: {frequenza} volte")
else:
    print(conteggio_coppie)
