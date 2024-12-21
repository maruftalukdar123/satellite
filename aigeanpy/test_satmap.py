import numpy as np
import os
import aigeanpy.net as net
from aigeanpy.satmap import SatMap, get_satmap
from pytest import approx
import pytest
from pathlib import Path


# ----------------------------
# Testing using correct inputs
# ----------------------------

#This tests the get_satmap fucntion which can return a object from filename correctly
def test_get_satmap():

    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa('aigean_lir_20221212_123848.asdf')

    image = get_satmap('aigean_lir_20221212_123848.asdf')
    assert image.metadata['date'] == '2022-12-12'
    assert image.metadata['xcoords'] == [0.0, 600]
    assert image.data.shape == (10, 20)

#Tests the meta function that can return the metadata correctly
def test_meta():
    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa('aigean_lir_20221212_123848.asdf')

    image = get_satmap('aigean_lir_20221212_123848.asdf')
    metadata = image.meta()
    assert metadata['date'] == '2022-12-12'
    assert metadata['xcoords'] == [0.0, 600]

#Tests the data function that can return the data correctly
def test_data():
    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa('aigean_lir_20221212_123848.asdf')

    image = get_satmap('aigean_lir_20221212_123848.asdf')
    assert image.data[0,0] == approx(293.62962963)

#Tests the fov function that can return the field of view correctly
def test_fov():
    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa('aigean_lir_20221212_123848.asdf')

    image = get_satmap('aigean_lir_20221212_123848.asdf')
    assert image.fov() == (600.0, 300.0)
 
#Tests the shape function that can return the shape of array correctly
def test_shape():
    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa('aigean_lir_20221212_123848.asdf')

    image = get_satmap('aigean_lir_20221212_123848.asdf')
    assert image.shape() == (10, 20)
 
#This tests that the fucntion that can provide the coordinates of centre correctly
def test_centre():

    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa('aigean_lir_20221212_123848.asdf')

    image = get_satmap('aigean_lir_20221212_123848.asdf')
    centre_coor = image.centre()
    assert centre_coor == (300.0, 150.0)

#This tests that the fucntion can provide the metadata and data in SatMap correctly after adding
def test_add():
    if os.path.exists('aigean_man_20230103_154956.hdf5') != True:
        net.download_isa("aigean_man_20230103_154956.hdf5")

    if os.path.exists('aigean_man_20230103_161956.hdf5') != True:
        net.download_isa('aigean_man_20230103_161956.hdf5')

    image1 = get_satmap('aigean_man_20230103_154956.hdf5')
    image2 = get_satmap('aigean_man_20230103_161956.hdf5')

    image_add = image1 + image2

    assert image_add.metadata['date'] == '2023-01-03'
    assert image_add.metadata['instrument'] == 'Manannan'
    assert all(image_add.metadata['xcoords'] == [  0., 900.])
    assert all(image_add.metadata['ycoords'] == [  0., 400.])
    assert image_add.data.shape == (27, 60)
    assert approx(image_add.data[0, -2]) == 224.56565656565658

#Tests the subtracting function that provides the metadata and data in SatMap correctly after adding
def test_subtract():
    if os.path.exists('aigean_lir_20221223_024822.asdf') != True:
        net.download_isa("aigean_lir_20221223_024822.asdf")

    if os.path.exists('aigean_lir_20230104_152610.asdf') != True:
        net.download_isa("aigean_lir_20230104_152610.asdf")

    image1 = get_satmap('aigean_lir_20221223_024822.asdf')
    image2 = get_satmap('aigean_lir_20230104_152610.asdf')

    image_sub = image1 - image2

    assert image_sub.metadata['instrument'] == 'Lir'
    assert all(image_sub.metadata['xcoords'] == [ 600., 1200.])
    assert all(image_sub.metadata['ycoords'] == [100., 300.])
    assert image_sub.data.shape == (7, 20)
    assert approx(image_sub.data[0, -3]) == -7.1380471380471135


#Tests the mosaic function that provides the metadata and data in SatMap correctly after subtracting
def test_mosaic_with_padding():
    if os.path.exists('aigean_lir_20221223_024822.asdf') != True:
        net.download_isa("aigean_lir_20221223_024822.asdf")

    if os.path.exists('aigean_man_20221223_030122.hdf5') != True:
        net.download_isa("aigean_man_20221223_030122.hdf5")

    image1 = get_satmap('aigean_lir_20221223_024822.asdf')
    image2 = get_satmap('aigean_man_20221223_030122.hdf5')

    image_mosaic = image1.mosaic(image2)

    assert all(image_mosaic.metadata['xcoords'] == [ 600., 1500.])
    assert all(image_mosaic.metadata["ycoords"] == [100., 500.])
    assert image_mosaic.metadata["resolution"] == 15
    assert image_mosaic.data.shape == (27, 60)
    assert approx(image_mosaic.data[1, -1]) == 326.73400673400675



#Tests the mosaic function that provides the metadata and data in SatMap correctly after subtracting
def test_mosaic_without_padding():
    if os.path.exists('aigean_lir_20221223_024822.asdf') != True:
        net.download_isa("aigean_lir_20221223_024822.asdf")

    if os.path.exists('aigean_man_20221223_030122.hdf5') != True:
        net.download_isa("aigean_man_20221223_030122.hdf5")

    image1 = get_satmap('aigean_lir_20221223_024822.asdf')
    image2 = get_satmap('aigean_man_20221223_030122.hdf5')

    image_mosaic = image1.mosaic(image2, padding = False )

    assert all(image_mosaic.metadata['xcoords'] == [ 600., 1200.])
    assert all(image_mosaic.metadata["ycoords"] == [100., 400.])
    assert image_mosaic.metadata["resolution"] == 15
    assert image_mosaic.data.shape == (20, 40)
    assert approx(image_mosaic.data[1, -1]) == 409.4276094276093

#Tests the visualize function that saves the image in png
def test_visualize_saving_image():
    if os.path.exists('aigean_lir_20221223_024822.asdf') != True:
        net.download_isa("aigean_lir_20221223_024822.asdf")

    image = get_satmap('aigean_lir_20221223_024822.asdf')

    image.visualize(save = True)
    image_path = Path('Aigean_Lir_20221223_024822.png').exists()
    assert image_path == True

# --------------------------
# Testing using wrong inputs
# --------------------------

#Test the get_satmap with wrong type of file
def test_wrong_type_file_get():
    with pytest.raises(FileNotFoundError):
        get_satmap("123.txt")


# Test that adding two image that is not a from the same instrument raises the correct error
def test_wrong_type_images_add():

    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa('aigean_lir_20221212_123848.asdf')

    if os.path.exists('aigean_man_20230103_154956.hdf5') != True:
        net.download_isa('aigean_man_20230103_154956.hdf5')

    image1 = get_satmap('aigean_lir_20221212_123848.asdf')
    image2 = get_satmap("aigean_man_20230103_154956.hdf5")

    with pytest.raises(TypeError):
        image_add = image1 + image2
    

#Test that adding two images that is not on the same data raises the correct error
def test_wrong_date_images_add():

    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa('aigean_lir_20221212_123848.asdf')
    
    if os.path.exists('aigean_lir_20230104_145310.asdf') != True:
        net.download_isa('aigean_lir_20230104_145310.asdf')
    
    image1 = get_satmap('aigean_lir_20221212_123848.asdf')
    image2 = get_satmap("aigean_lir_20230104_145310.asdf")

    with pytest.raises(TypeError):
        image_add = image1 + image2

#Test two images is not from the same instrument when operating subtracting
def test_subtract_wrong_instrument():
    if os.path.exists('aigean_lir_20221223_024822.asdf') != True:
        net.download_isa("aigean_lir_20221223_024822.asdf")

    if os.path.exists('aigean_man_20230104_153910.hdf5') != True:
        net.download_isa("aigean_man_20230104_153910.hdf5")

    image1 = get_satmap('aigean_lir_20221223_024822.asdf')
    image2 = get_satmap("aigean_man_20230104_153910.hdf5")

    with pytest.raises(TypeError):
        image_sub = image1 - image2

#Test two images is from the date when operating subtracting
def test_subtract_same_date():
    if os.path.exists('aigean_man_20230103_154956.hdf5') != True:
        net.download_isa("aigean_man_20230103_154956.hdf5")

    if os.path.exists('aigean_man_20230103_161956.hdf5') != True:
        net.download_isa("aigean_man_20230103_161956.hdf5")

    image1 = get_satmap('aigean_man_20230103_154956.hdf5')
    image2 = get_satmap('aigean_man_20230103_161956.hdf5')

    with pytest.raises(TypeError):
        image_sub = image1 - image2

#Test two images are not overlapping from the date when operating subtracting
def test_subtract_no_overlapping():
    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa('aigean_lir_20221212_123848.asdf')

    if os.path.exists('aigean_lir_20221223_024822.asdf') != True:
        net.download_isa('aigean_lir_20221223_024822.asdf')

    image1 = get_satmap('aigean_lir_20221212_123848.asdf')
    image2 = get_satmap('aigean_lir_20221223_024822.asdf')

    with pytest.raises(TypeError):
        image_sub = image1 - image2


# Test that two images is not on the same date for mosaic function and raise the correct error
def test_wrong_date_images_mosaic():

    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa('aigean_lir_20221212_123848.asdf')

    if os.path.exists("aigean_man_20230104_153910.hdf5") != True:
        net.download_isa("aigean_man_20230104_153910.hdf5")

    image1 = get_satmap('aigean_lir_20221212_123848.asdf')
    image2 = get_satmap("aigean_man_20230104_153910.hdf5")

    with pytest.raises(TypeError):
        image_mosaic = image1.mosaic(image2)


# Test that the wrong type of resolution raises the correct error
def test_wrong_type_resolution_mosaic():

    if os.path.exists('aigean_man_20230104_153910.hdf5') != True:
        net.download_isa('aigean_man_20230104_153910.hdf5')

    if os.path.exists("aigean_fan_20230104_152710.zip") != True:
        net.download_isa("aigean_fan_20230104_152710.zip")

    image1 = get_satmap('aigean_man_20230104_153910.hdf5')
    image2 = get_satmap("aigean_fan_20230104_152710.zip")

    with pytest.raises(TypeError):
        image_mosaic = image1.mosaic(image2, resolution= '1')

# Test that the wrong value of resolution raises the correct error
def test_wrong_value_resolution_mosaic():

    if os.path.exists('aigean_man_20230104_153910.hdf5') != True:
        net.download_isa('aigean_man_20230104_153910.hdf5')

    if os.path.exists("aigean_fan_20230104_152710.zip") != True:
        net.download_isa("aigean_fan_20230104_152710.zip")

    image1 = get_satmap('aigean_man_20230104_153910.hdf5')
    image2 = get_satmap("aigean_fan_20230104_152710.zip")

    with pytest.raises(ValueError):
        image_mosaic = image1.mosaic(image2, resolution= -1)

# Test that the wrong type of padding raises the correct error
def test_wrong_type_padding_mosaic():

    if os.path.exists('aigean_man_20230104_153910.hdf5') != True:
        net.download_isa('aigean_man_20230104_153910.hdf5')

    if os.path.exists("aigean_fan_20230104_152710.zip") != True:
        net.download_isa("aigean_fan_20230104_152710.zip")

    image1 = get_satmap('aigean_man_20230104_153910.hdf5')
    image2 = get_satmap("aigean_fan_20230104_152710.zip")

    with pytest.raises(TypeError):
        image_mosaic = image1.mosaic(image2, padding = -1)

# Test that resolution that is not in the right range of mosaic function would raise the correct error
def test_wrong_range_resolution_mosaic():

    if os.path.exists('aigean_man_20230104_153910.hdf5') != True:
        net.download_isa('aigean_man_20230104_153910.hdf5')

    if os.path.exists("aigean_fan_20230104_152710.zip") != True:
        net.download_isa("aigean_fan_20230104_152710.zip")

    image1 = get_satmap('aigean_man_20230104_153910.hdf5')
    image2 = get_satmap("aigean_fan_20230104_152710.zip")

    with pytest.raises(ValueError):
        image_mosaic = image1.mosaic(image2, resolution=10000)

#Test visualize function with wrong type of save input and correct error would raise
def test_wrong_save_type_visualise():

    if os.path.exists('aigean_lir_20221223_024822.asdf') != True:
        net.download_isa("aigean_lir_20221223_024822.asdf")

    image = get_satmap('aigean_lir_20221223_024822.asdf')
    with pytest.raises(TypeError):
        image.visualize(save = 1)

#Test visualize function with wrong type of savepath input and correct error would raise
def test_wrong_savepath_type_visualise():

    if os.path.exists('aigean_lir_20221223_024822.asdf') != True:
        net.download_isa("aigean_lir_20221223_024822.asdf")

    image = get_satmap('aigean_lir_20221223_024822.asdf')
    with pytest.raises(TypeError):
        image.visualize(save = True, savepath=1)

