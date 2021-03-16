import numpy as np
import matplotlib.pyplot as plt

a = [100]
b = [100]
fig = plt.figure(figsize=(24, 12))
plt.plot(1e7 / 531.5 - 1e7 / np.array(a), b, label='Ethanol')
#fig_manager = plt.get_current_fig_manager()
#fig_manager.window.showMaximized()
font1 = {'family': 'Calibri', 'weight': 'normal', 'size': 25}
plt.legend(prop=font1)
plt.title('Raman Spectra (532 nm)', size='30')
plt.tick_params(labelsize=16)
plt.xlabel('Raman Shift ($cm^{-1}$)', size=20)
plt.ylabel('Intensity (a.u.)', size=20)
plt.show()