# Tools for Nessie Circuits energy harvesting recorder

The energy harvesting recorder records voltage and current of two energy harvesters (AC and DC) as well as accelerometer readings.
The tools in this repository are used to convert recorded data to `csv` or `hdf` files for analysis and further processing.
There's also a command to convert a harvesting trace to a format compatible with the Nessie Circuits SolarBox.



## Installation

Install the python package using either

```
pip install nessie.recorder
```

or

```
pipenv install nessie.recorder
```


## Data extraction

To convert the file `REC_001.DAT` recorded with an EH recorder to a `csv` output file:

```
nessie-recorder extract -i REC_001.DAT -o out.csv
```

Extracting to `csv` requires to load all recorded data into memory, which may not work for very large files.

As an alternative, convert the file `REC_001.DAT` to an `hdf5` output file:

```
nessie-recorder extract -i REC_001.DAT -o out.h5
```

## Plotting

To plot the extracted data:

```
nessie-recorder plot -i out.csv
```

If your recording is very long, you won't be able to load all data into memory for plotting. If you extracted your data to `hdf5`, you can plot the downsampled (e.g., every 100th sample) data with:

```
nessie-recorder plot -i out.hdf5 -d 100
```

## Conversion to SolarBox

You can convert an EH recorder trace to a SolarBox trace to replay it to an energy harvesting device.
For this purpose, you will need a mapping of the SolarBox input value (0-100%) to the resulting power of a panel mounted inside.
This mapping must be formatted as a `csv` file with two columns: `solarbox` and `recorder` in percent and watts respectively.

```
solarbox,recorder
0,8.4833230555061e-08
10,0.00768804210057344
20,0.015250790089624976
30,0.022412615156234474
40,0.029180363344797327
```

With this mapping stored under `mapping.csv`, you can convert the recorder trace `recorded.csv` to a SolarBox trace `solarbox.csv` using:

```
nessie-recorder convert -i recorded.csv -o solarbox.csv -m mapping.csv
```

## Example Configuration

This directory also contains an example configuration file `./CONFIG.INI` for use with the EH recorder. Adjust it to your needs and store it on the top level of a FAT32-formatted SD Card under the name `CONFIG.INI`.