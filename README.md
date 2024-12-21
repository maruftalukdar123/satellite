# Package of aigeanpy

This is a package of aigeanpy, which can be used to analysis data from Aigean satellite.

## Installation

To install this package, you need to run the command below under the directory containing the package code.

```bash
pip install .
```

## Usage 

###  Getting the today image
If you want to get todays newest image from satellite, move to aigeanpy
```bash
cd aigeanpy
```
then:
```bash
aigean_today.py
```
if you want to specify an instrument
```bash
aigean_today.py -i lir
```
if you want to save the image
```bash
aigiean_today.py -i lir -s
```
### See the metadata for different files
If you want to see the metadata for a file, move to aigeanpy
```bash
cd aigeanpy
```
then
```bash
aigean_metadata.py aigean_lir_20221201_233614.asdf
```
If you want to see the metadata for multiple files at the same time, then list the file names one after the other
```bash
aigean_metadata.py aigean_lir_20221201_233614.asdf aigean_lir_20221201_230314.asdf
```


### Query the existed file on the website
If you want to query the file on the website, run the python code below
```python
from aigeanpy.net import query_isa

query_isa(satrt_date, stop_date, instrument)
```

### Download the existed file on the website
If you want to download the file on the website, run the python code below
```python
from aigeanpy.net import download_isa

download_isa(satrt_date, stop_date, instrument)
```

### Read the metadata
If you want to show the meadata of the file, you can invoke the tool with `aigean_metadata <filename>` or use python code below

```python
from aigean.satmap import get_satmap

image = get_satmap(filename)
metadata = image.metadata()
```

###  Getting the data in image
If you want to read the data of the file, you can use python code below

```python
from aigean.satmap import get_satmap

image = get_satmap(filename)
data = image.data()
```

###  Getting the field of view of image
If you want to get field of the view, you can use python code below

```python
from aigean.satmap import get_satmap

image = get_satmap(filename)
filed = image.fov()
```

###  Getting the centre of image
If you want to get centre of the view, you can use python code below

```python
from aigean.satmap import get_satmap

image = get_satmap(filename)
centre_coor = image.centre()
```

###  Add images (Combine two images) on the same date
If you want to add images from the same data and store the result in png, you can invoke the tool with `aigean_mosaic <required_resolution><first_filename> <second_filename>` or run the python code

```python
from aigean.satmap import get_satmap

image1 = get_satmap(first_filename)
imgae2 = get_satmap(second_filename)
image_mosaic = image1.mosaic(imgae2, resolution = required_resolution )
image_mosaic.visualize(save = True)

```
###  Add images (Combine two images) on the same date from the same instrument
If you want to add images from the same data and show the result, you can run the python code below.

```python
from aigean.satmap import get_satmap

image1 = get_satmap(first_filename)
imgae2 = get_satmap(second_filename)
image_add = imag1 + image2
image_mosaic.visualize()
```

Or if you want to save the result in .png, run the code below.

```python
from aigean.satmap import get_satmap

image1 = get_satmap(first_filename)
imgae2 = get_satmap(second_filename)
image_add = imag1 + image2
image_add.visualize(save = True)
```

###  Subtract images on the different dates from the same instrument
If you want to subtract images from the differents datas and show the result, you can run the python code below.

```python
from aigean.satmap import get_satmap

image1 = get_satmap(first_filename)
imgae2 = get_satmap(second_filename)
image_subtract = imag1 - image2
image_subtract.visualize()

```
Or if you want to save the result in .png, run the code below.

```python
from aigean.satmap import get_satmap


image1 = get_satmap(first_filename)
imgae2 = get_satmap(second_filename)
image_subtract = imag1 + image2
image_subtract.visualize(save = True)
```

###  Show a image or Store a image
If you want to show a image, you can run the python code below.
```python 
from aigean.satmap import get_satmap


image = get_satmap(first_filename)
image.visualize()
```

Or you want to store image in png.
```python 
image = get_satmap(first_filename)
image.visualize(save = True)
```
