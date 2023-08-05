# python-directplot

Educational library to directly plot single data points.

## Description

... to be added ...

## API

... to be added ...

## Development

### Build pypi package

Needed tools:

For Windows:

```
python -m pip install --upgrade build
python -m pip install --upgrade twine
```

For Linux:

```
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
```


Build package:

```
python -m build
```

Upload package to pypi:

```
twine upload dist/*
```
