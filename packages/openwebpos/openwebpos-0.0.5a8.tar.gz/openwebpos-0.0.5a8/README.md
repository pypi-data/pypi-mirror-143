# OpenWebPOS

OpenWebPOS is a web-based point of sale system written in python using the Flask framework.

## Installation

Run the following to install:
```bash
$ pip install openwebpos
```

## Usage

```python
from openwebpos import OpenWebPOS

application = OpenWebPOS()

if __name__ == "__main__":
    application.run()
```



# Developing

To install openwebpos, along with the tools you need to develop and run tests, run the following in your virtualenv:
```bash
$ pip install -e .[dev]
```