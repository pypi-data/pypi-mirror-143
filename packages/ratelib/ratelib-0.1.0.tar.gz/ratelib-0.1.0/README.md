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
Default way to get `ratelib` is to download it from PyPI:
```
  pip install ratelib
```

Classes
-------
- **Library:** Collection of reaction rates, database itself
- **Rate:** Reaction rate class with properties from REACLIB format
- **RateFilter:** Class for filtering rates in Library
- **Nucleus:** Basic class to unify different nucleus denotions
