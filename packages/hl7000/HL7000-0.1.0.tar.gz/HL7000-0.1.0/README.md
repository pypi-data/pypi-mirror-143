# HL7000

This library is made to help consolidate measurements from the SebaKMT HL7000 acoustic logger.

The goal is to centralize the data into measurement folders, provide an index for your measurement folders and to prevent duplicate records being saved.

## Install

    pip install HL7000

## Usage

The format will be a single depth folder structure, in which each folder name will be a uuid to prevent collision.

An index file will be created after saving a measurement, and can be rebuilt/saved using `save_index()`

All files will be copied from the source folder (likely off the HL7000) to the target folder when saving.


### Single Measurement usage

To read and process a single measurement

```
from HL7000 import Measurement

measurement = Measurement('/path/to/measurement')

# view dataframe
measurement.data

#save to folder
measurement.save_measurement('/path/to/save/folder')
```

### Multiple Measurement usage

To save multiple items, simply pass the source folder and target folders

```
from HL7000 import load_folder

load_folder('/path/to/source/folder', '/path/to/target/folder')
```

### Rebuilding index

Index can be rebuilt for a folder if any error or deletion occurs

```
from HL7000 import save_index

save_index('/path/to/folder')
```

### Import Folder from command line

```
python -m HL7000 /path/to/source/folder /path/to/target/folder
```


## Future Plans

* Companion GIS library for processing GIS data
* Visulization Components
    * FFT of each measurements
    * Time series of each measurement
    * Overlays of multiple measurements
