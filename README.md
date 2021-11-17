# wfslib

https://pypi.org/project/wfslib/
https://wfslib.readthedocs.io/en/latest/


wfslib is open library for wave front data processing:

* different data type usage (hfd, bim, numpy);
* automatic geometry calculation;
* offsets calculation;
* settings-tools for manage yours data.

### Code example
`from wfslib.wfs import WFSData`

`wfs = WFSData('../data/subpixel_test.h5', dataset_name = 'wfss/n0/detector') #Load data`

`p = wfs.geometry.options #Geometry options`
`print(p)`
`wfs.reference = 8`

#Change geometry options

`wfs.geometry.set_options(shift=(-p['start_point'][0]+1,-p['start_point'][1]+1), border = 0, cell_width = p['cell_width']-1)`

#Visualization

`wfs.show_geometry()`

### Results

`{'border': 4.0, 'cell_width': 110.0, 'start_point': [168, 131]}`


