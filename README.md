Scripts for adding roof information to open street map
======================================================

Input
-----
The file `roof_types_sxm.csv` contains the data from a manually mapped session. This data has been mapped on aerial imagery in an offline ID-editor setup. Purpose of this script is adding this data to osm.

The data already contains osm id's so spatial joining is not needed.

Scripts
-------

1. Run `csv_clean_up.py` to remove all unnecessary information (empty rows and unused columns) and cast our values to the ones used by osm. This scripts outputs `roof_types_sxm_clean.csv`.

2. Download `buildings_sxm_input.osm` using overpass turbo with the following query:
```
﻿[out:xml][timeout:25];
// gather results
(
  // query part for: “building=*”
  node["building"](17.99979487484851,-63.15679550170898,18.126112640728326,-62.99491882324219);
  way["building"](17.99979487484851,-63.15679550170898,18.126112640728326,-62.99491882324219);
  relation["building"](17.99979487484851,-63.15679550170898,18.126112640728326,-62.99491882324219);
);
(._;>;);
out meta;
```
3. Run `add_rooftypes.py` which will add the roof shapes and materials to the osm objects, only if they do not exist in osm yet. The output is called `buildings_sxm_output.osm`.

4. Upload the data from `buildings_sxm_output.osm` by using JOSM.

Workflow
-------
![alt text](https://github.com/rodekruis/osm_rooftypes_sxm/blob/master/St_maarten_workflow.png)


