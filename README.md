[![Build Status](https://travis-ci.com/ladybug-tools/uwg-schema.svg?branch=master)](https://travis-ci.com/ladybug-tools/uwg-schema)
[![Coverage Status](https://coveralls.io/repos/github/ladybug-tools/uwg-schema/badge.svg?branch=master)](https://coveralls.io/github/ladybug-tools/uwg-schema)

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

# uwg-schema

:city_sunrise: :scroll: Input schema for the [Urban Weather Generator (UWG)](https://github.com/ladybug-tools/uwg).

## Installation

```console
pip install uwg-schema
```

## QuickStart

```python
import uwg_schema

```

## API Documentation

[Model Schema](https://ladybug-tools.github.io/uwg-schema/model.html)

[Simulation Parameter Schema](https://ladybug-tools.github.io/uwg-schema/simulation-parameter.html)

## Local Development

1. Clone this repo locally

```console
git clone git@github.com:ladybug-tools/uwg-schema

# or

git clone https://github.com/ladybug-tools/uwg-schema
```

2. Install dependencies:

```console
cd uwg-schema
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

3. Run Tests:

```console
python -m pytest tests/
```

4. Generate Documentation:

```python
python ./docs.py
```

5. Generate Sample Files:

```python
python ./scripts/export_samples.py
```
