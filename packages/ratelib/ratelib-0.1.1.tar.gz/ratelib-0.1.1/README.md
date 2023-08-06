ratelib
=======

A simple interface to handle REACLIB format databases of astrophysical
reaction rates.

Standard REACLIB database can be downloaded from here: 
https://reaclib.jinaweb.org

Requirements
------------
- Python 3.5+
- numpy
- scipy

Installation
------------
Package `ratelib` can be installed via `pip`:
```
  pip install ratelib
```
You can also install the most recent version from the git repository with 
following commands:
```
  git clone https://github.com/kompoth/ratelib
  cd ratelib
  python -m build
  pip install dist/*.whl
```

Usage
-----
A simple script `example.py` is located in the root of the git repository.
It loads a version of REACLIB, provided as the first argument, and draws
a nuclei chart of weak decay rates at the temperature of 1 GK.

This script requires `matplotlib>=3.4`.

Classes
-------
- **Library:** Collection of reaction rates, database itself
- **Rate:** Reaction rate class with properties from REACLIB format
- **RateFilter:** Class for filtering rates in Library
- **Nucleus:** Basic class to unify different nucleus denotions
