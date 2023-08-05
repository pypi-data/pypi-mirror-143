# ClearLIFE Server SDK

`clearlife` allows you to build server applications on ClearOS server
that leverage best-of-class key management using derived keys. Users
connect their ClearNODE to derived keys from the ClearLIFE mobile app
on ClearPHONE. Just like any app on the ClearPHONE can use the SDKs
to get decentralized identity support (using derived keys), any server
app can get derived keys from ClearLIFE server using this SDK.

## Quickstart

First, install the package from PyPI:

```
pip install clearlife
```

The easiest way to use the SDK from python is to create an instance of 
the client for your application:

```python
from clearlife import ClearLifeClient
client = ClearLifeClient("com.company.product")
```

You can then grab derived keys using a single line of python code:

```python
context = "context" # Currently limited to 8 bytes.
keys = client.derive(context, 0)
```

## CLI

There is also a command-line interface for the SDK that is installed in `bin`
as `clearlife`. To get started with it, do:

```
clearlife --examples
```

It also has a well-documented help via `-h` or `--help`.