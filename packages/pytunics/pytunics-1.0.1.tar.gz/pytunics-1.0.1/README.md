# Tunics Laser package
This is simple package for self studying GIT and\
control instrument by GPIB interface.

# Installation
pip install pytunics
# Usage example
```python
from pytunics import TunicsLaser
from numpy import arange

wl_start = 1550.1
wl_stop = 1550.3
wl_step = 0.01
las = TunicsLaser()
las.enable()
for wl in arange(wl_start, wl_stop, wl_step):
    las.set_wavelength(wl)
    # do something
las.disable()
```

#Special thanks
\
Artem Nedbailo - QA advices & reviews\
Yann Leventoux - Instrument & tools supply

#TBD

CI/CD
