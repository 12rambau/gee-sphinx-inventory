# gee-sphinx-inventory

The code used to generate the sphinx inventory of the GEE objects.

## Usage

This repository is generating and storing the Sphinx inventory of the GEE objects.
The inventory is generated by the `generate_inventory.py` script.
The script is using the `ee` module to get the list of the objects and their methods.
The inventory is stored in the `inventory/earthengine-api.inv` file.
The `inventory.json` file is used by the `sphinx` to generate the documentation.

To link Earth Engine object in your sphinx documentation, add the following to your `conf.py` file:

```python
intersphinx_mapping = {
    'ee': (
        "https://developers.google.com/earth-engine/apidocs",
        "https://raw.githubusercontent.com/gee-community/sphinx-inventory/refs/heads/main/inventory/earthengine-api.inv"
    ),
}
```

Then you can use the `:py:class:'ee.Image'` role to link the Earth Engine object in your Sphinx files.
It will appear as [`ee.Image`](https://developers.google.com/earth-engine/apidocs/ee-image) in the built documentation.

```rst

> [!NOTE]
> - To know more about `earthengine-api` read their documentation [here](https://developers.google.com/earth-engine)
> - To know more about `sphinx` read their documentation [here](https://www.sphinx-doc.org/en/master/)
> - To know more about `sphinx.ext.intersphinx` usage read their documentation [here](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html)
```
