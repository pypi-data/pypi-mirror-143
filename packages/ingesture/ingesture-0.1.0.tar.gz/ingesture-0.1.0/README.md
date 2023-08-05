# ingesture
Ingest gesturally-structured data into models with multiple export

This package is **not** even close to usable, and is just a sketch at the moment.
If for some reason you see it and would like to work on it with me, feel free to
open an issue :)


# Declare your data

Even the most disorganized data system has *some* structure. We want to be able
to recover it without demanding that the entire acquisition process be reworked

To do that, we can use a family of specifiers to tell `ingest` where to get metadata

```python
from datetime import datetime
from ingesture import Schema, spec
from pydantic import Field

class MyData(Schema):
    # parse metadata in a filename
    subject_id: str = Field(..., 
        description="The ID of a subject of course!",
        spec = spec.Path('electrophysiology_{subject_id}_*.csv')
    )
    # parse multiple values at once
    date: datetime
    experimenter: str
    date, experimenter = Field(...,
        spec = spec.Path('{date}_{experimenter}_optodata.h5')
    )
    
    
    # from inside a .mat file
    other_meta: int = Field(...
        spec = spec.Mat(
            path='**/notebook.mat', # 2 **s mean we can glob recursively
            field = ('nb', 1, 'user') # index recursively through the .mat
        )
    )
    # and so on
```

Then, parse your schema from a folder

```python
data = MyData.make('/home/lab/my_data')
```

Or a bunch of them!

```python
data = MyData.make('/home/lab/my_datas/*')
```

## Multiple Strategies

`todo`

## Hierarchical Modeling

Our data is rarely a single type, often there is a repeatable substructure that
is paired with different macro-structures: eg. you have open-ephys data within a directory
with behavioral data in one experiment and paired with optical data in another.

Make submodels and recombine them freely...

`todo`


# Export Data

Once we have data in an abstract model, then we want to be able to export it to
multiple formats! To do that we need an interface that describes
the basic methods of interacting with that format (eg. .csv files are
written differently than hdf5 files) and a mapping from our model fields
to locations, attributes, and names in the target format.

## Pydantic base export

### json

## From the Field specification

```python
class MyData(Schema):
    subject_id: str = Field(
        spec = ...,
        nwb_field = "NWBFile:subject_id"
    )
```

## From a `Mapping` object

```python

class NWB_Map(Mapping):
    subject_id = 'NWBFile:subject_id'

class MyData(Schema):
    subject_id: str = Field(...)
    
    __mapping__ = NWB_Map

```
    