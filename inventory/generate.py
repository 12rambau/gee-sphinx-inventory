"""The code used to generate the sphinx inventory of the GEE objects"""
import json
from pathlib import Path
import inspect
import logging

import sphobjinv as soi
import ee

HERE = Path(__file__).parent
"""The current folder"""

logger = logging.getLogger(__name__)
"""The logger for this module"""

# create the inventory object
logger.info("Generating the inventory file")
inv = soi.Inventory()

# add package information from the ee lib
logger.info("Adding the package information")
inv.project = "earthengine-api"
inv.version = ee.__version__

# add the main module manually
logger.info("Adding the main module")
inv.objects.append(soi.DataObjStr(
    name = ee.__name__,
    domain = "py",
    role = str(type(ee)),
    priority = "1",
    uri = "",
    dispname = "-",
))

# Not all the objects from ee should be added to the inventory as most of them are undocumented
# the list have been carefully built manually and saved in a json file. For each object, all the methods
# are added to the inventory. Some of them might not be documented but they will be removed thanks to
# user feedback.
logger.info("Adding the main classes and methods")
class_list = json.loads((HERE / "ee_class_list.json").read_text())
public_members = lambda obj: [o for n, o in inspect.getmembers(obj) if not n.startswith("_")]
for class_name in class_list:

    # first inject the class itself
    cls = getattr(ee, class_name)
    atoms = ["ee", class_name]
    inv.objects.append(soi.DataObjStr(
        name = ".".join(atoms),
        domain = "py",
        role = "class",
        priority = "1",
        uri = "-".join(atoms).lower(),
        dispname = "-",
    ))

    # then all its downstream methods
    method_list = public_members(cls)
    for meth in method_list:
        atoms = ["ee", class_name, meth.__name__]
        inv.objects.append(soi.DataObjStr(
            name = ".".join(atoms),
            domain = "py",
            role = "method",
            priority = "1",
            uri = "-".join(atoms).lower(),
            dispname = "-",
        ))

# Initialize and Authenticate even if they start with a capital letter are not objects but
# functions that must be documented
logger.info("Adding the 2 oauth functions")
for func in ["Initialize", "Authenticate"]:
    atoms = ["ee", func]
    inv.objects.append(soi.DataObjStr(
        name = ".".join(atoms),
        domain = "py",
        role = "function",
        priority = "1",
        uri = "-".join(atoms).lower(),
        dispname = "-",
    ))

# From the ee.data module, only the methods should be added into the inventory as the rest is
# undocumented so it reduces vastly the number of items to update
logger.info("Adding the data module")
meth_list = [o for n, o in inspect.getmembers(ee.data) if not (n.startswith("_") or inspect.isclass(o) or n[0].isupper())]
for meth in meth_list:
    atoms = ["ee", "data", meth.__name__]
    inv.objects.append(soi.DataObjStr(
        name = ".".join(atoms),
        domain = "py",
        role = "method",
        priority = "1",
        uri = "-".join(atoms).lower(),
        dispname = "-",
    ))

# batch module is only embeding 5 abstract classes that manage exportation processes.
# The rest should remain undocumented
logger.info("Adding the batch module")
batch_classes = public_members(ee.batch.Export)
for cls in batch_classes:
    method_list = public_members(cls)
    for meth in method_list:
        atoms = ["ee", "batch", "Export", cls.__name__, meth.__name__]
        inv.objects.append(soi.DataObjStr(
            name = ".".join(atoms),
            domain = "py",
            role = "method",
            priority = "1",
            uri = "-".join(atoms[2:]).lower(),
            dispname = "-",
        ))

# export the file as a inventory file in the repository
logger.info("Writing the inventory file")
text = inv.data_file(contract=True)
ztext = soi.compress(text)
soi.writebytes(str(HERE/"earthengine-api.inv"), ztext)

logger.info(f"Inventory file generated with {len(inv.objects)} objects.")
