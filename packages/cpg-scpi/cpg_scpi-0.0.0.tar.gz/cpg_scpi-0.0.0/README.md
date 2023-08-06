# cpg_scpi

Educational client library to use Adafruit Circuit Playground via SCPI protocol in Python3.


## Description

The corresponding Arduino Sketch for the Circuit Playground can be found [here](https://github.com/GeorgBraun/SCPI-for-Adafruit-Circuit-Playground).

... more docu to come ...





## Development

### Build pypi package

Tools needed to build and publish to PyPi under Windows:

```
python -m pip install --upgrade build
python -m pip install --upgrade twine
```

Tools needed to build and publish to PyPi Linux/MacOS:

```
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
```


Build package:

```
python -m build
```

Upload package to pypi:

Before uploading, delete outdated build artifacts in the `dist` folder, such that only the latest build files are uploaded.

```
twine upload dist/*
```
