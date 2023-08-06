# df_jupyter_magic

`%df` magic commands to get file usage within JupyterLab notebook. This package utilizes python function `shutil.disk_usage()`.

## Requirements

- JupyterLab >= 3.0
- Python >= 3.6

## Install

To install this package, execute:
```
pip install df_jupyter_magic
```

## Uninstall
To remove the package, execute:
```
pip uninstall df_jupyter_magic
```

## How to Use
You must first import the package by running following command:
```python
import df_jupyter_magic
```

Then, you may use one of the following commands:

- `%df` returns a human readable string in GB. Input is the path to the disk/partition. 
- `%df --raw` returns a raw data object.
- `%df --on` returns rsults in a string in GB after every subsequent cell run.
- `%df --off` turns off `on`.
- `%df -p /` sets the path to the partition to check.
- `%df -v` prints off additional text for debugging.
