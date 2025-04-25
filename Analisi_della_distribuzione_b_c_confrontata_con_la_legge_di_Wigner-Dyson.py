import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import rv_histogram
from collections import Counter  # Importa la classe Counter


def preparaArray(file_content):
    array = []
    s = file_content.split("\n")

    for riga in s:
        if riga != '':
            vector = riga.split(" ")
            # Assicurati che ci siano abbastanza elementi prima di accedere agli indici
            if len(vector) >= 4:
                p = vector[1].replace(',', '.')
                b = vector[2].replace(',', '.')
                c = vector[3].replace(',', '.')
                array.append([float(p), float(b), float(c)])
            else:
                print(f"Riga ignorata (meno di 4 elementi): {riga}")  # Messaggio di debug
    return array


# Funzione per calcolare le differenze e generare l'istogramma
def analizza_distribuzione_differenze(file_path="D://Documenti//----Numeri//Codice Python//testFile.txt"):  # Assumo sia nella stessa directory
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

        data_array = preparaArray(file_content)

        # Ora creiamo un DataFrame pandas da data_array
        df = pd.DataFrame(data_array)

        b = df.iloc[:, 1].values
        c = df.iloc[:, 2].values
        delta_p = b + c

        # Calcola l'istogramma delle differenze
        hist, bin_edges = np.histogram(delta_p, bins='auto', density=True)

        # Calcola i punti medi dei bin
        bin_mids = (bin_edges[:-1] + bin_edges[1:]) / 2

        return hist, bin_mids, bin_edges  # Restituisco anche bin_edges

    except FileNotFoundError:
        return None, None, None  # Restituisco None per tutti e tre


# Esegui l'analisi
hist, bin_mids, bin_edges = analizza_distribuzione_differenze()

# Verifica se l'analisi ha avuto successo prima di procedere
if hist is None:
    print("Errore: Impossibile trovare il file o errore durante l'analisi.")
    exit()  # Esci dal programma o gestisci l'errore come preferisci

print("Valore di hist:", hist)
print("Valore di bin_mids:", bin_mids)
print("Valore di bin_edges:", bin_edges)

if isinstance(hist, np.ndarray) and len(hist) > 0:
    # Calcola la larghezza delle barre solo se hist è un array e bin_edges ha almeno 2 elementi
    if len(bin_edges) > 1:
        bar_width = bin_edges[1] - bin_edges[0]
    else:
        bar_width = 1.0

    # Visualizza l'istogramma
    plt.figure(figsize=(10, 6))
    plt.bar(bin_mids, hist, width=bar_width)
    plt.title('Distribuzione di Δp = b + c')
    plt.xlabel('Valore di Δp')
    plt.ylabel('Densità di Probabilità')
    plt.show()

    # Ulteriore analisi: confronto con Wigner-Dyson (opzionale)
    # Nota: Per un confronto accurato, avresti bisogno di una distribuzione Wigner-Dyson teorica
    # con cui confrontare. Questo è complesso e dipende dai parametri specifici
    # del sistema.
    # Qui mostro solo un esempio concettuale di come potresti procedere.
    # Esempio concettuale: Genera una distribuzione casuale per confronto
    # In pratica, dovresti usare una distribuzione Wigner-Dyson teorica appropriata
    rng = np.random.default_rng()
    wigner_dyson_sample = rng.normal(size=1000)
    wd_hist, wd_bin_edges = np.histogram(wigner_dyson_sample, bins='auto', density=True)
    wd_bin_mids = (wd_bin_edges[:-1] + wd_bin_edges[1:]) / 2

    # Visualizza la distribuzione di confronto
    plt.figure(figsize=(10, 6))
    if len(wd_bin_edges) > 1:
        wd_bar_width = wd_bin_edges[1] - wd_bin_edges[0]
    else:
        wd_bar_width = 1.0
    plt.bar(wd_bin_mids, wd_hist, width=wd_bar_width, alpha=0.5, label='Wigner-Dyson (Esempio)')
    plt.title('Confronto con Wigner-Dyson')
    plt.xlabel('Valore')
    plt.ylabel('Densità di Probabilità')
    plt.legend()
    plt.show()

else:
    print("Errore durante l'analisi della distribuzione. Impossibile visualizzare l'istogramma.")
    print(delta_p)  # Stampa l'errore o i dati grezzi, se disponibili
