# From prompt: pip install fsspec
import pandas as pd
import numpy as np
from collections import Counter  # Importa la classe Counter

from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

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
                print(f"Ignored line (less than 4 items): {riga}")  # Messaggio di debug
    return array


def analisi_fourier(file_path="testFile.txt"):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

        data_array = preparaArray(file_content)

        df = pd.DataFrame(data_array)

        b_values = df.iloc[:, 1].tolist()
        c_values = df.iloc[:, 2].tolist()

        fft_b = fft(b_values)
        fft_c = fft(c_values)

        freq_b = fftfreq(len(fft_b))
        freq_c = fftfreq(len(fft_c))

        potenza_b = np.abs(fft_b)**2
        potenza_c = np.abs(fft_c)**2

        return freq_b, potenza_b, freq_c, potenza_c

    except FileNotFoundError:
        return "Error: File Not Found!"
    except Exception as e:
        return f"Error while processing: {e}"

freq_b, potenza_b, freq_c, potenza_c = analisi_fourier()

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(freq_b, potenza_b)
plt.title('Spettro di Potenza di b')
plt.xlabel('Frequenza')
plt.ylabel('Potenza')

plt.subplot(1, 2, 2)
plt.plot(freq_c, potenza_c)
plt.title('Spettro di Potenza di c')
plt.xlabel('Frequenza')
plt.ylabel('Potenza')

plt.tight_layout()
plt.show()
