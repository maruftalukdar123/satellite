import aigeanpy.net as net
from pathlib import Path
import pytest


# ---------------------
# Testing net.query_isa
# ---------------------

# Test that the passing no arguments work
def test_no_arguments():
    sol = net.query_isa()
    assert sol == 'http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/', "Did not request with the right url"


# Test that only passing each instrument separately works
@pytest.mark.parametrize('instrument_for_test,url',
[
    ('Lir','http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/?instrument=Lir'),
    ('Manannan','http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/?instrument=Manannan'),
    ('Fand','http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/?instrument=Fand'),
    ('Ecne','http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/?instrument=Ecne')
]

)
def test_only_instruments(instrument_for_test,url):
    sol = net.query_isa(instrument=instrument_for_test)
    assert sol == url, "Did not request with the right url"


# Test that passing a non-existing instrument outputs the right error message
def test_wrong_instrument():
    sol = net.query_isa(instrument='na')
    assert sol == "Instrument na doesn't exist in this archive","Did not get the expected error message"


# Test that passing all arguments work
def test_all_arguments():
    sol = net.query_isa(start_date='2022-12-12',stop_date='2022-12-13',instrument='Fand')
    assert sol == 'http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/?start_date=2022-12-12&stop_date=2022-12-13&instrument=Fand', "Did not request with the right url"


# Testing that passing a date range greater than 3 days outputs the right error message
def test_large_date_range():
    sol = net.query_isa(start_date='2022-12-12',stop_date='2022-12-17')
    assert sol == "Range requested too long - this service is limited to 3 days","Did not get the expected error message"


# Another form of testing too large of a date range,
# This time, checking for the right error message when the stop_date is not given,
# Which automatically defaults to 2022-12-19 as described in the docstring
def test_large_date_range_stop_date_not_provided():
    sol = net.query_isa(start_date='2022-12-12')
    assert sol == "Range requested too long - this service is limited to 3 days","Did not get the expected error message"


# Testing that passing only a stop_date outputs the correct error messgage
def test_only_stop_date():
    sol = net.query_isa(stop_date='2022-12-12')
    assert sol == "One or multiple arguments provided are not accepted in this service. Only start_date, stop_date and instrument are accepted","Did not get the expected error message"



# Test that passing wrong input typers raises the right error for all arguments
# Checking 3 input types
# int, float and boolean


# Ask wether this is actually implementing all of the arguments,
# intrument, star_date and end_date or just one argument
@pytest.mark.parametrize('inputs',
[
    (2),
    (0.5),
    (True),
]
)

def test_wrong_type_instrument(inputs):
    with pytest.raises(TypeError):
        net.query_isa(instrument=inputs)
    with pytest.raises(TypeError):
        net.query_isa(start_date=inputs)
    with pytest.raises(TypeError):
        net.query_isa(stop_date=inputs)



# ------------------------
# Testing net.download_isa
# ------------------------

# SELF_NOTE: Everytime the following tests are run, files will be downloaded
# in the current directory, a new_dir in the current direcoty and 
# in the C:\Users\44740\Desktop\Computing directory.
# These are needed to test that downloads are happening. 
# For now, manually delete the files, later implement auto-delete

# Test that with no save_dir given, downloads in the current directory
# The filename of the file we'll download is 'aigean_lir_20221218_065812.asdf'
def test_no_save_dir():
    net.download_isa(filename='aigean_lir_20221218_065812.asdf')
    is_downloaded = Path('aigean_lir_20221218_065812.asdf').exists()
    assert is_downloaded == True, "File not downloaded or not downloaded in the current directory (as expected by default) or downloaded with the wrong name"


# Test that with save_dir pointing to a not existing direcotry,
# function should raise NameError
# SELF_NOTE: Should it be a name_error?
def test_non_existing_directory():
    with pytest.raises(NameError):
        net.download_isa(filename='aigean_lir_20221218_065812.asdf',save_dir=r'Computing')
