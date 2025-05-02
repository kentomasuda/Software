# -*- coding: utf-8 -*-
"""
Dendrogram main

https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.dendrogram.html

@author: MURAKAMI Tamotsu
@date: 2019-02-21
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster import hierarchy

print('* start *')

ytdist = np.array([662., 877., 255., 412., 996., 295., 468., 268., 400., 754., 564., 138., 219., 869., 669.])
Z = hierarchy.linkage(ytdist, 'single')
print('Z=', Z)
plt.figure()
dn = hierarchy.dendrogram(Z)

hierarchy.set_link_color_palette(['m', 'c', 'y', 'k'])
fig, axes = plt.subplots(1, 2, figsize=(8, 3))
dn1 = hierarchy.dendrogram(Z, ax=axes[0], above_threshold_color='y', orientation='top')
dn2 = hierarchy.dendrogram(Z, ax=axes[1], above_threshold_color='#bcbddc', orientation='right')
hierarchy.set_link_color_palette(None)  # reset to default after use
plt.show()

print('* end *')

# End of file