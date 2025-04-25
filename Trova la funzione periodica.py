import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.optimize import curve_fit

# Carica i dati dal foglio Excel
file_path = 'D:\\Documenti\\----Numeri\\funzione periodica NP_1.xlsx'  
# Sostituisci con il percorso del tuo file
df = pd.read_excel(file_path, sheet_name='funzione_periodica_NP_1')
data = df['NP_1'].dropna().values  # Colonna con i tuoi dati

# Grafico della sequenza originale
plt.figure(figsize=(12, 6))
plt.plot(data, marker='o', linestyle='-', color='b')
plt.title("Sequenza di valori in 'NP_1'")
plt.xlabel("Indice")
plt.ylabel("Valore")
plt.grid()
plt.show()

# Trasformata di Fourier per trovare la frequenza dominante
fft_values = fft(data)
fft_magnitude = np.abs(fft_values)

# Grafico della magnitudine FFT
plt.figure(figsize=(12, 6))
plt.stem(fft_magnitude[:len(fft_magnitude)//2])
#prevede l'upgrade del matplotlib
#plt.stem(fft_magnitude[:len(fft_magnitude)//2], use_line_collection=True)
plt.title("Spettro della trasformata di Fourier di 'NP_1'")
plt.xlabel("Indice di frequenza")
plt.ylabel("Magnitudine")
plt.grid()
plt.show()

# Trova la frequenza dominante
freq_index = np.argmax(fft_magnitude[1:len(fft_magnitude)//2]) + 1
dominant_period = len(data) / freq_index
estimated_frequency = 1 / dominant_period

# Modello sinusoidale per adattamento
def sinusoidal_model(x, amplitude, frequency, phase, offset):
    return amplitude * np.sin(2 * np.pi * frequency * x + phase) + offset

# Fit del modello
x_data = np.arange(len(data))
initial_guess = [np.std(data), estimated_frequency, 0, np.mean(data)]
params, _ = curve_fit(sinusoidal_model, x_data, data, p0=initial_guess)
amplitude, frequency, phase, offset = params

# Genera i dati di adattamento
fitted_data = sinusoidal_model(x_data, amplitude, frequency, phase, offset)

# Grafico dei dati originali e della funzione approssimata
plt.figure(figsize=(12, 6))
plt.plot(x_data, data, label='Dati Originali', color='b', marker='o', linestyle='-')
plt.plot(x_data, fitted_data, label='Funzione Sinusoidale Adattata', color='r', linestyle='--')
plt.title("Dati Originali e Funzione Sinusoidale Approssimata")
plt.xlabel("Indice")
plt.ylabel("Valore")
plt.legend()
plt.grid()
plt.show()

# Stampa i parametri della funzione
print("Ampiezza:", amplitude)
print("Frequenza:", frequency)
print("Fase:", phase)
print("Offset:", offset)