# Purview Python #

## Description ##

This package is meant to act as a wrapper for the MSFT Purview (and Apache Atlas) APIs. It is currently in development by [Spydernaz](https://github.com/Spydernaz). To set up a development instance in Apache Atlas, you can see this repo [here]()

## Installation ##

This package runs on python3 and above. To install run

```sh
pip3 install purview_py
```

## Configuration ##

Describe the config Steps

## Example Usage ##

The follow code will connect to your purview instance and fetch the `hive_table` type. From here you could modify some details and then update your server as shown in the second part of this snippet

```python
import purview_py

# Your configuration
CLIENT_ID = __YOUR_CLIENT_ID__
CLIENT_SECRET = __YOUR_CLIENT_SECRET__
TENANT_ID = __YOUR_TENANT_ID__

resource =__YOUR_RESOURCE__

# Create a connection to your resource
conn = purview_py.PurviewConnection(resource, purview_py.TokenAuth(CLIENT_ID, CLIENT_SECRET, TENANT_ID))

# Fetch the hive_table type
t = purview_py.PurviewType.getTypeByName(conn, "hive_table")

# Add some new attributes to the type

# Update the Type in Purview

```

## Docs ##

