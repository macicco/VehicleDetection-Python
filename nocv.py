#!/usr/bin/env python
import h5py
from argparse import ArgumentParser
from pathlib import Path
import numpy as np
from matplotlib.pyplot import figure, draw, pause

from datetime import datetime



def main():
    p = ArgumentParser()
    p.add_argument('infn', help='HDF5 motion file to analyze')
    p.add_argument('-wcount', help='write blob count stem')
    p.add_argument('-v', '--verbose', help='show debug plots', action='store_true')
    p = p.parse_args()


    verbose = p.verbose

    fn = Path(p.infn).expanduser()

    with h5py.File(fn, 'r') as f:
        mot = np.rot90(f['motion'][1025:,...].astype(np.uint8), axes=(1,2))

    bmot = mot > 15

    ax1 = figure(1).gca()
    countfn = fn.parent/p.wcount if p.wcount else None

    Ncount = []
    for i, m in enumerate(bmot):
        ax1.cla()
        ax1.imshow(m, origin='bottom')
        ax1.set_title(f'frame {i}')

        N = fourier(m, i, verbose)

        Ncount.append(N)


        if countfn is not None and i and not i % 500:
            countfn = fn.parent/(p.wcount + datetime.now().isoformat()[:-7] + '.h5')
            with h5py.File(countfn, 'w') as f:
                f['count'] = Ncount
                f['index'] = i
            Ncount = []


def fourier(mot: np.ndarray, i: int, verbose: bool=False) -> int:
    """
    rectangular LPF in effect (crude but fast)
    """
    MIN = 5
    MAX = np.inf

    lane1 = mot[4:10, :].sum(axis=0)
    lane2 = mot[10:16, :].sum(axis=0)

    L = lane1.size
    iLPF = (L*2//5, L*3//5)  # arbitrary

    Flane1 = abs(np.fft.fft(lane1))**2
    Flane2 = abs(np.fft.fft(lane2))**2

    N1 = int(MIN <= Flane1[iLPF[0]:iLPF[1]].sum() <= MAX)
    N2 = int(MIN <= Flane2[iLPF[0]:iLPF[1]].sum() <= MAX)

    if verbose:
        ax = figure(2).gca()
        ax.cla()
        ax.plot(np.fft.fftshift(Flane1))
        ax.plot(np.fft.fftshift(Flane2))
        ax.set_title(f'frame {i}  counts {N1} {N2}')
        ax.set_ylim(0, 100)
        ax.axvline(iLPF[0], color='red', linestyle='--')
        ax.axvline(iLPF[1], color='red', linestyle='--')

        draw()
        pause(0.1)


    return N1 + N2




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass