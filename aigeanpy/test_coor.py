import aigeanpy.net as net
from aigeanpy.coor import coor
import pytest
import os

# ---------------------------------
# Testing using correct coordinate
# ---------------------------------

#This tests that function can correctly converting pixel coordinates to earth coordinates at simple case
def test_pixel_to_earth_with_valid_coordinate():
    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa('aigean_lir_20221212_123848.asdf')
    eaarth_coords = coor.pixel_to_earth('aigean_lir_20221212_123848.asdf', (1,1))
    assert eaarth_coords == (45.0, 255.0)

#This tests that function can correctly converting pixel coordinates to earth coordinates at edge case
def test_edge_pixel_to_earth_with_valid_coordinate():
    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa('aigean_lir_20221212_123848.asdf')
    eaarth_coords = coor.pixel_to_earth('aigean_lir_20221212_123848.asdf', (0,3))
    assert eaarth_coords == (105.0, 285.0)

#This tests that function can correctly converting earth coordinates to pixel coordinates at simple case
def test_earth_to_pixel_with_valid_coordinate():
    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa('aigean_lir_20221212_123848.asdf')
    pixel_coords = coor.earth_to_pixel('aigean_lir_20221212_123848.asdf', (300.0, 150.0))
    assert pixel_coords == (5,9)

#This tests that function can correctly converting earth coordinates to pixel coordinates at edge case
def test_edge_earth_to_pixel_with_valid_coordinate():
    if os.path.exists('aigean_lir_20221212_123848.asdf') != True:
        net.download_isa('aigean_lir_20221212_123848.asdf')
    pixel_coords = coor.earth_to_pixel('aigean_lir_20221212_123848.asdf', (105.0, 285.0))
    assert pixel_coords == (0,3)


# ---------------------------------
# Testing using wrong coordinate
# ---------------------------------

@pytest.mark.parametrize("filename, coordinates",
[
    ('aigean_lir_20221212_123848.asdf', 1), # Test that passing a coordinate that is not a tuple raises the correct error
    ('aigean_lir_20221212_123848.asdf', (1,2,3)) # Test that passing a coordinate that do not has two elements raises the correct error
    
]
)

def test_wrong_type_pixel_to_earth(filename, coordinates):
    with pytest.raises(TypeError):
        coor.pixel_to_earth(filename, coordinates)


@pytest.mark.parametrize("filename, coordinates",
[
    ('aigean_lir_20221212_123848.asdf', (-1, -1)), # Test that passing a coordinate that is not in the range of shape raises the correct error
    ('aigean_lir_20221212_123848.asdf', (1000, 1000)) # Test that passing a coordinate that is not in the range of shape raises the correct error
    
]
)

def test_wrong_twrnage_pixel_to_earth(filename, coordinates):
    with pytest.raises(ValueError):
        coor.pixel_to_earth(filename, coordinates)

@pytest.mark.parametrize("filename, coordinates",
[
    ('aigean_lir_20221212_123848.asdf', 1), # Test that passing a coordinate that is not a tuple raises the correct error
    ('aigean_lir_20221212_123848.asdf', (1,2,3)) # Test that passing a coordinate that do not has two elements raises the correct error
    
]
)

def test_wrong_type_earth_to_pixel(filename, coordinates):
    with pytest.raises(TypeError):
        coor.earth_to_pixel(filename, coordinates)



@pytest.mark.parametrize("filename, coordinates",
[
    ('aigean_lir_20221212_123848.asdf', (1000, 1000)) # Test that passing a coordinate that is not in the range raises the correct error
    
]
)

def test_wrong_twrnage_pixel_to_earth(filename, coordinates):
    with pytest.raises(ValueError):
        coor.earth_to_pixel(filename, coordinates)
