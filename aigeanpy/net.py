from argparse import ArgumentParser
from requests import get
from pathlib import Path
from os.path import isdir




def query_isa(start_date :str = None , stop_date :str = None, instrument :str = None) -> str:
    '''This function prints results from the ISA data archive query service as
    JSON files and returns the url of the query.

    The parameters accepted are the same ones as the ISA data archive query service.

    Notes
    -----
        - Queries larger than three days are not allowed.
        - If stop_date is set, then start_date must also be set, as in start_date is no longer optional.

    Parameters
    ----------
    start_date: str (date in format YYYY-mm-dd), optional
                sets the starting date to search for data in the Aigean archive,
                by default None for the function (which defaults to 2022-12-19 for the query service).
    
    stop_date: str (date in format YYYY-mm-dd), optional
                sets the stop date (inclusive) to search in the Aigean archive,
                by default None for the function (which defaults to 2022-12-19 for the query service).
    
    instrument: str, optional
                one of the possible instruments: 'Lir', 'Manannan', 'Fand' or 'Ecne',
                by default None for the function (which defaults to all the instruments in the query service).


    Returns
    -------
    str
        the url that takes to the results of the query.
    '''

    # Type checking for arguments.
    # Not needed for command line arguments, as they are by default, strings.

    # If arguments in wrong format or date range too long or non-existing instrument is given,
    # then the query service itself returns an error message. So the format of the arguments itself
    # does not need to be checked by this function.

    if start_date and type(start_date) != str:
        raise TypeError ('Start_date must be a string in format YYYY-mm-dd')

    if stop_date and type(stop_date) != str:
        raise TypeError ('Stop_date must be a string in format YYYY-mm-dd')

    if instrument and type(instrument) != str:
        raise TypeError ("Instrument must be a string and one of 'Lir', 'Manannan', 'Fand' or 'Ecne'")


    payload = {'start_date':start_date , 'stop_date':stop_date , 'instrument':instrument}

    timeout = 5

    try:
        r = get('http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query',params=payload, timeout=timeout)
    except:
        raise TimeoutError('No internet connection')
    else:
    

        # If r.json() returns an error message, then print the error message and also return it.
        # Else print the json file line by line, then return the url used to find the query.
        # This will be used for tests, and also allows the users to manually perform the query.
        for i in r.json():
            if i == 'message':
                error_message = r.json()['message']
                print(error_message)
                return error_message
            else:
                print(i)

        return r.url


def download_isa(filename, save_dir=None):
    '''given a filename (from running the net.query_isa() function),
    downloads the file, by default in the current directory.

    Parameters
    ----------
    filename : string
                the filename of the file to download, (from running the net.query_isa() function)
    
    save_dir : string or path object, optional
                Given save_dir, downloads the file in the directory pointed by save_dir.
                by default None for the function (which downloads to the current working directory)
    '''


    payload = {'filename':filename}
    r = get('https://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/download',params=payload)
    
    if save_dir:
        path = Path(save_dir)

        # path.exists() is used to check if save_dir is an immediate
        # sub-direcotry in the folder this script is.
        # this will also work if save_dir is just the name of the direcotry
        # doesn't necessarily have to be a path.
        
        # isdir checks any directory in any place in the computer
        # but has to be path object. 
            
        if not path.exists() or not isdir(save_dir):
            raise NameError(f"Directory pointed by {save_dir} doesn't exist")

        open(f"{save_dir}/{filename}", "wb").write(r.content)
    
    else:
        open(f"{filename}", "wb").write(r.content)
        