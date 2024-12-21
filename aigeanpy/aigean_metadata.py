from argparse import ArgumentParser
import os
import aigeanpy.net as net
from aigeanpy.satmap import SatMap, get_satmap


def aigean_metadata(filename):
    '''Given a filename or a list of filenames, function first
    downloads the files if necessary. Then displays the metadata
    of each file in the order they were passed in.

    If the metadata failed to show for any of the files, then
    it will also display a list of files that failed.

    Parameters
    ----------
    filename : str or list[str]
        files whos metadata to display. Must be an aigeanpy file
        and be of type asdf, hdf5 or zip
    '''

    if type(filename) == str:
        filename = [filename]
    
    elif type(filename) == list:
        for i in filename:
            if type(i) != str:
                raise TypeError('Each filename must be of type string')

    else:
        raise TypeError('filename must be of type string')
    wrong_file = []

    for file in filename:

        extension = os.path.splitext(file)[1]
        if extension not in ['.asdf', '.hdf5', '.zip']:
            wrong_file.append(file)
            continue

        try:
            
            if os.path.exists(file) != True:
                net.download_isa(file)

            sat_map_object = get_satmap(file)

        except:
            wrong_file.append(file)

        else:
            metadata = sat_map_object.meta()

            
            if extension == '.asdf':

                del metadata['asdf_library']
                del metadata['history']
            
            if len(filename) == 1:
                for dict_elem in metadata:
                    print(f'{dict_elem}: {metadata[dict_elem]}')
            else:
                for dict_elem in metadata:
                    print(f'{file}:{dict_elem}: {metadata[dict_elem]}')
            
            print()


    if wrong_file:
        print('These files failed while being processed:')
        for i in wrong_file:
            print(f'- {i}\n')



def cli():
    '''Creates command line interface that calls on the aigean_metadata function.
    '''
    parser = ArgumentParser(description="Download the lates image from the ISA archives")
    parser.add_argument('filename', type=str, nargs='+')

    arguments = parser.parse_args()
    aigean_metadata(arguments.filename)

if __name__ == '__main__':
    cli()