# -*- coding: utf-8 -*-

import numpy as np

huge1 = np.random.rand(2000000)
huge2 = np.random.rand(2000000)

dist = np.linalg.norm(huge1-huge2)

print(dist)
