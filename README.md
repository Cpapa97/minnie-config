# minnie-config
Synced universal configuration for working with the `microns_minnie65_%` schemas with external and their attribute adapters.

## Installation

```bash
pip3 install git+https://github.com/cajal/minnie-config.git
```

## Usage

Before initializing the schema or a virtual module of the schema

```python
import minfig
from minfig.adapters import * # Required for the adapters to be used with locally defined tables

minfig.configure_minnie()
```

or

```python
from minfig import * # This will also import the attribute adapters into the namespace

minfig.configure_minnie()
```

To create a virtual schema with the proper attribute adapters

```python
import minfig

minnie = minfig.configure_minnie(return_virtual_module=True)
```

or a more manual version

```python
import datajoint as dj
from minfig import adapter_objects # included with wildcard imports

minnie = dj.create_virtual_module('minnie', 'microns_minnie65_01', add_objects=adapter_objects)
```
