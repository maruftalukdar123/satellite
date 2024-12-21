from argparse import ArgumentParser
import aigeanpy.net as net
from aigeanpy.satmap import SatMap, get_satmap
import os
import sys


def aigean_mosaic(resolution, filename):
    '''Given a resolution and a list of files, function will download
    the files if necessary, then create and save a mosaic with those files.

    Parameters
    ----------
    resolution : int
        The resolution to use when creating the mosaic

    filename : list[str]
        The list of files to use to create a mosaic. Must be an aigeanpy file
        and be of type asdf, hdf5 or zip
    '''

    for file in filename:
        extension = os.path.splitext(file)[1]
        if extension not in ['.asdf', '.hdf5', '.zip']:
            sys.exit('Filetype must be one of asdf, hdf5 or zip')

    try:
        if os.path.exists(filename[0]) != True:
            net.download_isa(filename[0])

        A = get_satmap(filename[0])

        mosaic_results = [A]
        for i in range(len(filename)-1):
            
            if os.path.exists(filename[i+1]) != True:
                net.download_isa(filename[i+1])
                
            B = get_satmap(filename[i+1])
            AB = mosaic_results[-1]
            AB = AB.mosaic(B, resolution=resolution)
            mosaic_results.append(AB)
        
        mosaic_results[-1].visualize(save=True)
    
    except:
        sys.exit('Mosaic could not be done. This could be because one (or more) of the files is not an aigeanpy file or has been corrupted')
        


def cli():
    '''Creates a command line interface that calls the aigean_mosaic function.
    '''
    parser = ArgumentParser(description="Download the lates image from the ISA archives")
    parser.add_argument('-r', '--resolution', type=int, help='The resolution of mosaic picture as an integer')
    parser.add_argument('filename', type=str, nargs='+', help='List of the filenames to create a mosaic with')

    arguments = parser.parse_args()
    aigean_mosaic(arguments.resolution, arguments.filename)

if __name__ == '__main__':
    cli()