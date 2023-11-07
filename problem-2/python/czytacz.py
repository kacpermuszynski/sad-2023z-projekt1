import numpy as np
import matplotlib.pyplot as plt
import os

def read_and_plot(filename):
    BajtowNaLiczbe = 4
    LiczbaLiczb = os.path.getsize(filename) / BajtowNaLiczbe

    with open(filename, 'rb') as f:
        v = np.fromfile(f, dtype=np.float32)

    print(v[:10])
    plt.plot(v[:100000])
    plt.show()

    idx = np.arange(67650, 67900)
    plt.plot(idx, v[idx])
    plt.show()

read_and_plot('signal_50MHz.bin')