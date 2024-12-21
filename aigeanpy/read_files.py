import asdf
import h5py
import zipfile
import json
import numpy
from io import BytesIO
import csv
import os
from os import getcwd
from os.path import isfile, splitext
import aigeanpy.net as net




# read_asdf opens an asdf file using the python asdf library
# and saves all of its data in a dictionary called metadata.
# data is then extracted and deleted from the metadata dictionary

def read_asdf(filename): 
    """ Read an ASDF file and return metadata and data of image

    Parameters
    ----------
    filename: str
            name of the file to read, such as aigean_lir_20221223_024822.asdf

    Returns
    -------
    return1: dictionary
            The information of image

    return2: ndarray
            data of image

    Examples
    --------
    >>> if os.path.exists('aigean_lir_20221212_123848.asdf') != True: net.download_isa("aigean_lir_20221212_123848.asdf")
    >>> metadata, data = read_file('aigean_lir_20221212_123848.asdf')
    >>> metadata['xcoords']
    [0.0, 600.0]
    >>> data.shape 
    (10, 20)
    """

    metadata = dict(asdf.open(filename))
    data = numpy.array(metadata["data"])
    del metadata["data"]

    return metadata, data


# read_h5py reads a hdf5 file. 
# For the ISA case the dataset is stored in the 'observation',
# and the metadata is stored as attributes of 'observation'.

def read_h5py(filename):
    """ Read a h5py file and return metadata and data of image

    Parameters
    ----------
    filename: str
            name of the file to read, such as aigean_man_20221212_123848.hdf5

    Returns
    -------
    return1: dictionary
            The information of image

    return2: ndarray
            data of image

    Examples
    --------
    >>> net.download_isa('aigean_man_20221212_123848.hdf5')
    >>> metadata, data = read_file('aigean_man_20221212_123848.hdf5')
    >>> metadata['xcoords']
    array([  0., 450.])
    >>> data.shape 
    (10, 30)
    """

    f = h5py.File(filename, 'r')
    metadata = dict(f['observation'].attrs)
    data = numpy.array(f['observation']['data'])

    return metadata, data


# read_zip uses the BytesIO function to temporarily store the contents 
# of the zip file. A 'ZipFile' object is then created using that content.
# The separate files of the initial zip file can now be read.

# Metadata is stored in metdata.json
# and the data is stored in observation.npy

def read_zip(filename):
    """ Read a zip file from fand instrument and return metadata and data of image
    
    Parameters
    ----------
    filename: str
            name of the file to read, such as aigean_fan_20221212_123848.zip

    Returns
    -------
    return1: dictionary
            The information of image

    return2: ndarray
            data of image

    Examples
    --------
    >>> net.download_isa('aigean_fan_20221212_123848.zip')
    >>> metadata, data = read_file('aigean_fan_20221212_123848.zip')
    >>> metadata['xcoords']
    [75.0, 300.0]
    >>> data.shape 
    (10, 45)
    """
    with open(filename, "rb") as f:

        content = f.read()
        ob = BytesIO(content)
        zip_ob = zipfile.ZipFile(ob)

        metadata= zip_ob.read("metadata.json")
        metadata = json.loads(metadata)

        data = zip_ob.read("observation.npy")
        data = BytesIO(data)
        data = numpy.load(data, allow_pickle=True )

    return metadata, data



def read_csv(filename):
    """ Read a csv file from fand instrument and return the data of csv
    
    Parameters
    ----------
    filename: str
            name of the file to read, such as aigean_fan_20221212_123848.zip

    Returns
    -------
    return1: list
            Store the turbulence

    return2: list
            Store the salinity

    return3: list
            Algal density

    Examples
    --------
    >>> net.download_isa("aigean_ecn_20221212_123848.csv")
    >>> turbulence, salinity, algal_density = read_file('aigean_ecn_20221212_123848.csv')
    >>> round(turbulence[0], 2)
    -0.14
    >>> round(salinity[-1], 2)
    7.46
    >>> round(algal_density[2], 2)
    -2.68
    """
    with open(filename,'r') as f:
        csv_reader = csv.reader(f, delimiter=',')

        turbulence, salinity, algal_density = [], [], []

        for row in csv_reader:
            turbulence.append(float(row[0]))
            salinity.append(float(row[1]))
            algal_density.append(float(row[2]))

        return numpy.array(object=[turbulence,salinity,algal_density])


# Determines the type of file (given a file name)
# Then extracts data using the functions defines above
def read_file(filename):
    """  Determine the type of the file and return metadata and data of image
    
    Parameters
    ----------
    filename: str
            name of the file to read, such as aigean_fan_20221212_123848.zip

    Returns
    -------
    return1: dictionary
            The information of image

    return2: ndarray
            data of image
    """

    if type(filename) != str:
        raise TypeError('Argument "filename" must be of type string')

    current_working_directory = getcwd()
    file_exists = isfile(path=(current_working_directory+'/'+filename))


    if not file_exists:
        raise FileNotFoundError ("The file must exists be in the current working directory")

    extension = splitext(filename)[1]

    if extension == '.asdf':
        return read_asdf(filename)

    elif extension == '.hdf5':
        return read_h5py(filename)

    elif extension == '.zip':
        return read_zip(filename)

    elif extension == '.csv':
        return read_csv(filename)

    else:
        raise FileNotFoundError ("The file must be in the current working directory and must be of type ASDF, HDF5, zip or csv")

