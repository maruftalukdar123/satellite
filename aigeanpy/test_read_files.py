import aigeanpy.net as net
from aigeanpy.read_files import read_file
import os
import pytest

# -------------------------------
# Testing using correct filenames
# -------------------------------

# To do the following tests, we first need to download 1 of each type
# of file (asdf, hdf5, zip and csv).

# This tests that correctly giving an existing asdf file,
# it reads the correct metadata and data.
def test_read_asdf_with_valid_filename():
    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa("aigean_lir_20221212_123848.asdf")
    metadata, data = read_file('aigean_lir_20221212_123848.asdf')
    assert metadata['date'] == '2022-12-12', 'The date exctracted from the asdf file metadata is different than expected'
    assert metadata['xcoords'] == [0.0, 600], 'The x-coordinates extracted from the asdf file metadata is different than expected'
    assert data.shape == (10, 20), 'The shape of the data in the asdf is different than expected'


# This tests that correctly giving an existing hdf5 file,
# it reads the correct metadata and data.
def test_read_hdf5_with_valid_filename():
    net.download_isa('aigean_man_20221212_123848.hdf5')
    metadata, data = read_file('aigean_man_20221212_123848.hdf5')
    assert metadata['date'] == '2022-12-12', 'The date exctracted from the hdf5 file metadata is different than expected'
    assert all(metadata['xcoords'] == [0.0, 450]), 'The x-coordinates extracted from the hdf5 file metadata is different than expected'
    assert data.shape == (10, 30), 'The shape of the data in the hdf5 is different than expected'



# This tests that correctly giving an existing zip file,
# it reads the correct metadata and data.
def test_read_zip_with_valid_filename():
    net.download_isa('aigean_fan_20221212_123848.zip')
    metadata, data = read_file('aigean_fan_20221212_123848.zip')
    assert metadata['date'] == '2022-12-12', 'The date exctracted from the zip file metadata is different than expected'
    assert metadata['xcoords'] == [75, 300], 'The x-coordinates extracted from the zip file metadata is different than expected'
    assert data.shape == (10, 45), 'The shape of the data in the zip file is different than expected'


# This tests that correctly giving an existing csv file,
# it correctly separates and reads the three pieces of data
def test_read_csv_with_valid_filename():
    net.download_isa('aigean_ecn_20221212_123848.csv')
    turbulence, salinity, algal_density = read_file('aigean_ecn_20221212_123848.csv')
    assert turbulence[0] == -0.1411, 'The first measurement of the turbolence is different than expected'
    assert salinity[-1] == 7.46459, 'The last measurement of the salinity is different than expected'
    assert algal_density[2] == -2.67752, 'The third measurement of the algal density is different than expected'



# ---------------------------------
# Testing using incorrect filenames
# ---------------------------------


@pytest.mark.parametrize('filename',
[
    ('aigean_ecn_20221212_123848.pdf'), # Test that passing a file with the wrong extension raises the correct error
    ('aigean_ecn_20221212_123848'), # Test that passing a file with no extension raises the correct error
    ('no_file_name.asdf') # Test that passing an inexisting file raises the correct error
]
)

def test_wrong_and_no_extension(filename):
    with pytest.raises(FileNotFoundError):
        read_file(filename)


@pytest.mark.parametrize('filename',
[
    (1), # Test that passing an integer filename raises the correct error
    (1.02), # Test that passing a float filename raises the correct error
    (True) # Test that passing a boolean filename raises the correct error
]
)

def test_filenames_of_different_types(filename):
    with pytest.raises(TypeError):
        read_file(filename)