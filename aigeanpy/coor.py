from aigeanpy.read_files import read_file
import os
import aigeanpy.net as net



class coor():

    def pixel_to_earth(filename, coordinates):

        """ Convert the pixel coordinates to earth coordinates and return the earth coordinates

        Parameters
        ----------
        filename: str
                  name of the file to read, such as aigean_lir_20221223_024822.asdf
        
        coordinates: tuple
                     pixel coordinates, such as (0, 1)

        Returns
        -------
        tuple
            The coordinates in earth coordinates

        Examples
        --------
        >>> if os.path.exists('aigean_lir_20221212_123848.asdf') != True: net.download_isa("aigean_lir_20221212_123848.asdf")
        >>> coor.pixel_to_earth('aigean_lir_20221212_123848.asdf', (1,1))
        (45.0, 255.0)
        """


        if type(coordinates) != tuple or len(coordinates) != 2:
            raise TypeError ("The type of coordinates must be tuple in format of (x, y)")

        if type(coordinates[0]) != int or type(coordinates[1]) != int:
            raise TypeError ("The number in coordinates must be integer")

        metadata, data = read_file(filename)
        array_shape = data.shape
        xcoords = metadata['xcoords']
        ycoords = metadata['ycoords']
        resolution = metadata['resolution']
    

        if coordinates[0] < 0 or coordinates[0] > (array_shape[0]-1):
            raise ValueError ("The value of pixel coordinates is out of range")

        if coordinates[1] < 0 or coordinates[1] > (array_shape[1]-1):
            raise ValueError ("The value of pixel coordinates is out of range")

        x_earth = xcoords[0] + coordinates[1]*resolution + 0.5*resolution
        y_earth = ycoords[1] - coordinates[0]*resolution - 0.5*resolution

        earth_coords = (x_earth, y_earth)

        return earth_coords


    def earth_to_pixel(filename, coordinates):

        """ Convert the earth coordinates to pixel coordinates and return the pixel coordinates

        Parameters
        ----------
        filename: str
                  name of the file to read, such as aigean_lir_20221223_024822.asdf
        
        coordinates: tuple
                     earth coordinates, such as (10, 15)

        Returns
        -------
        tuple
            The coordinates in pixel coordinates

        Examples
        --------
        >>> if os.path.exists('aigean_lir_20221212_123848.asdf') != True: net.download_isa("aigean_lir_20221212_123848.asdf")
        >>> coor.earth_to_pixel('aigean_lir_20221212_123848.asdf', (300.0, 150.0))
        (5.0, 9.0)
        """

        # If the earth coordinates is in the center of four pixels, the coordinates of pixels 
        # with earth coordinates at top right corner of pixels would be selected to convert.

        if type(coordinates) != tuple or len(coordinates) != 2:
            raise TypeError ("The type of coordinates must be tuple in format of (x, y)")

        metadata, data = read_file(filename)
        array_shape = data.shape
        xcoords = metadata['xcoords']
        ycoords = metadata['ycoords']
        resolution = metadata['resolution']

        if coordinates[0] < xcoords[0] or coordinates[0] > xcoords[1]:
            raise ValueError ("The value of earth coordinates is out of range")

        if coordinates[1] < ycoords[0] or coordinates[1] > ycoords[1]:
            raise ValueError ("The value of earth coordinates is out of range")

        if coordinates[1] == ycoords[0]:          
            x_pixel = ((ycoords[1] - coordinates[1])//resolution) - 1 

        else:
            x_pixel = (ycoords[1] - coordinates[1])//resolution


        y_reminder = (coordinates[0]-xcoords[0])%resolution

        if coordinates[0] == xcoords[1] or y_reminder == 0:
            if coordinates[0] == xcoords[0]:
                
                y_pixel = (coordinates[0]-xcoords[0])//resolution 

            else:
                y_pixel = ((coordinates[0]-xcoords[0])//resolution) - 1 

        else:
            y_pixel = (coordinates[0]-xcoords[0])//resolution

        pixel_coords = (x_pixel, y_pixel)

        return pixel_coords









    