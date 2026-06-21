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
            if len(vector) >= 4:
                p = vector[1].replace(',', '.')
                b = vector[2].replace(',', '.')
                c = vector[3].replace(',', '.')
                array.append([float(p), float(b), float(c)])
            else:
                print(f"Ignored line (less than 4 items): {riga}")  
    return array


def analizza_distribuzione_differenze(file_path="testFile.txt"):  

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

        data_array = preparaArray(file_content)

        df = pd.DataFrame(data_array)

        b = df.iloc[:, 1].values
        c = df.iloc[:, 2].values
        delta_p = b + c

        hist, bin_edges = np.histogram(delta_p, bins='auto', density=True)

        bin_mids = (bin_edges[:-1] + bin_edges[1:]) / 2

        return hist, bin_mids, bin_edges  

    except FileNotFoundError:
        return None, None, None  


hist, bin_mids, bin_edges = analizza_distribuzione_differenze()

if hist is None:
    print("Error: Cannot find file or error while parsing.")
    exit()  

print("Valore di hist:", hist)
print("Valore di bin_mids:", bin_mids)
print("Valore di bin_edges:", bin_edges)

if isinstance(hist, np.ndarray) and len(hist) > 0:
    if len(bin_edges) > 1:
        bar_width = bin_edges[1] - bin_edges[0]
    else:
        bar_width = 1.0

    plt.figure(figsize=(10, 6))
    plt.bar(bin_mids, hist, width=bar_width)
    plt.title('Distribuzione di Δp = b + c')
    plt.xlabel('Valore di Δp')
    plt.ylabel('Densità di Probabilità')
    plt.show()

    rng = np.random.default_rng()
    wigner_dyson_sample = rng.normal(size=1000)
    wd_hist, wd_bin_edges = np.histogram(wigner_dyson_sample, bins='auto',    
                                                                                            density=True)
    wd_bin_mids = (wd_bin_edges[:-1] + wd_bin_edges[1:]) / 2

    # Visualizza la distribuzione di confronto
    plt.figure(figsize=(10, 6))
    if len(wd_bin_edges) > 1:
        wd_bar_width = wd_bin_edges[1] - wd_bin_edges[0]
    else:
        wd_bar_width = 1.0
    plt.bar(wd_bin_mids, wd_hist, width=wd_bar_width, alpha=0.5, 
                                                          label='Wigner-Dyson (Esempio)')
    plt.title('Confronto con Wigner-Dyson')
    plt.xlabel('Valore')
    plt.ylabel('Densità di Probabilità')
    plt.legend()
    plt.show()

else:
    print("Errore durante l'analisi della distribuzione. “ +
                                           ”Impossibile visualizzare  l'istogramma.")
    print(delta_p)  # Stampa l'errore o i dati grezzi, se disponibili

