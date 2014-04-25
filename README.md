typekit-python
==============

This is a (minimal) Python module that implements the Typekit developers API. It allows you to create, retrieve, delete, update, and publish Typekit kits in Python. 

There is currently no support for:
- Retrieving library and family information
- Pip installation

But they are on the roadmap.

## Usage

Currently, there is no support for Pip installation. For now, you can use it by cloning the repository.

```
git clone git@github.com:suchanlee/typekit-python.git
```

Initialize the client with your developer API token. You can get your API token [here](https://typekit.com/account/tokens). All method calls return the JSON representation of the return from calling the Typekit API.

```
from typekit import Typekit

tk = Typekit(api_token='<API token>')
```
### List kits

To list all your kits, use the following command:

```
tk.list_kits()
```

### Get kit

To get information about a specific kit, input the kit id as the argument:

```
tk.get_kit(kit_id='<kit_id>')
```

### Create kit

To create a new kit, use the method `create_kit(name, domains, families=None, badge=False)`. `Name` and `domains` fields are required, but the `families` and `badge` fields are not.

The arguments are in the following format:
- **name**: string
- **domains**: string of format 'localhost, http://domain.com, 127.0.0.1' or a Python list of strings of format ['localhost', 'http://domain.com', '127.0.0.1']
- **families**: list of dictionaries with the following key : values
  - 'id' : font family id (string)
  - (optional) 'variations' : comma separated variations (string).

An example of the families format is: `families = [{'id': 'ftnk', 'variations': 'n3,n4'}, {'id': 'pcpv', 'variations': 'n4'}]` in which case we would create a kit with the font families Futura-PT and Droid Sans with font variations normal 3 (font-weight:300 and not italicized or strong), normal 4 and normal 4, respectively.

Example usage:

```
name = 'example typekit kit'
domains = ['localhost', 'http://domain.com']
families = [{'id': 'ftnk', 'variations': 'n3,n4'}, {'id': 'pcpv', 'variations': 'n4'}]

tk.create_kit(name, domains, families)
```

### Update kit

To create a new kit, use the method `update_kit(kit_id, name=None, domains=None, families=None, badge=False)`. The only required field is `kit_id`. `Name`, `domains`, `families` and `badge` fields are not required.

Field formats are the same as `create_kit`.

Example usage:

```
tk.update_kit(kit_id='<kit_id>', name='new name', badge='true')
```

### Remove kit

To remove a kit, use the method `remove_kit(kit_id)`. The `kit_id` field is required.

```
tk.remove_kit(kit_id='<kit_id>')
```

### Publish kit

To publish a kit, use the method `publish_kit(kit_id)`. The `kit_id` field is required.
```
tk.publish_kit(kit_id='<kit_id>')
```
