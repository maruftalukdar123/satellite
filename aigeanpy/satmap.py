from aigeanpy.read_files import read_file
import matplotlib.pyplot as plt
import aigeanpy.net as net
from skimage.transform import rescale, downscale_local_mean
from pathlib import Path
import numpy as np
import os


def get_satmap(filename):
    """Function to generate SatMap object
    Parameters
    ----------
    filename: string
            The name of the file
    Returns
    -------
    object
            An object to manipulate the data
        """

    extension = os.path.splitext(filename)[1]
    
    if extension == '.csv':
        data = read_file(filename)
        return SatMap(data)
    
    elif extension == '.asdf' or extension == '.hdf5' or extension == '.zip':
        metadata, data = read_file(filename)
        return SatMap(data,metadata)
    
    else:
        raise FileNotFoundError ("The file must be in the current working directory and must be of type ASDF, HDF5, zip or csv")
    
    

class SatMap:
    """An object to manipulate the data
        Parameters
        ----------
        self: object
                Object of SatMap to be set up
        
        data: ndarray
                Array to store the data in the file
        
        metadata: dictionary
                The default value of metadata is None. Store the information of file if the file has the metadata.
            """
    def __init__(self,data, metadata=None) -> None:
        self.data = data
        self.metadata = metadata

    def __str__(self):
        boottom_left = (self.metadata['xcoords'][0], self.metadata['ycoords'][0])
        top_right = (self.metadata['xcoords'][1], self.metadata['ycoords'][1])
        info = "<" + self.metadata["observatory"] + "/" + self.metadata["instrument"] + ":" + " " + str(boottom_left) + " - " + str(top_right) + " " + str(self.metadata["resolution"]) + " m/px>"
        return info

    def meta(self):
        """Get the metadata of image
        Parameters
        ----------
        self: object
                Object of SatMap
        
        Returns
        -------
        dictionary
            A dicionary includes metadata of the image
        Examples
        --------
        >>> if os.path.exists('aigean_lir_20221212_123848.asdf') != True: net.download_isa('aigean_lir_20221212_123848.asdf')
        >>> image = get_satmap('aigean_lir_20221212_123848.asdf')
        >>> image.metadata['xcoords']
        [0.0, 600.0]
        """
        if self.metadata:
            return self.metadata
        else:
            raise TypeError('You are trying to read the metadata of a csv file, which does not exist')

    
    def data(self):
        """Get the field of view of image in earth coordinates
        Parameters
        ----------
        self: object
                Object of SatMap
        
        Returns
        -------
        tuple
            A tuple of two float numbers representing field of view of image in earth coordinates
        Examples
        --------
        >>> if os.path.exists('aigean_lir_20221212_123848.asdf') != True:net.download_isa('aigean_lir_20221212_123848.asdf')
        >>> image = get_satmap('aigean_lir_20221212_123848.asdf')
        >>> round(image.data[0,0])
        294
        """
        
        return self.data

    def fov(self):
        """Get the field of view of image in earth coordinates
        Parameters
        ----------
        self: object
                Object of SatMap
        
        Returns
        -------
        tuple
            A tuple of two float numbers representing field of view of image in earth coordinates
        Examples
        --------
        >>> if os.path.exists('aigean_lir_20221212_123848.asdf') != True: net.download_isa('aigean_lir_20221212_123848.asdf')
        >>> image = get_satmap('aigean_lir_20221212_123848.asdf')
        >>> image.fov()
        (600.0, 300.0)
        """

        if self.metadata:
            field_of_view = (
                self.metadata['xcoords'][1]-self.metadata['xcoords'][0],
                self.metadata['ycoords'][1]-self.metadata['ycoords'][0]
            )
            
            return field_of_view
        else:
            raise TypeError('It looks like you are trying to obtain the field of fiew from a file whose metadata is not available')


    def shape(self):
        """Get the shape of the array of data
        Parameters
        ----------
        self: object
                Object of SatMap
        
        Returns
        -------
        tuple
            A tuple of two integers representing shape of data
        Examples
        --------
        >>> if os.path.exists('aigean_lir_20221212_123848.asdf') != True: net.download_isa('aigean_lir_20221212_123848.asdf')
        >>> image = get_satmap('aigean_lir_20221212_123848.asdf')
        >>> image.shape()
        (10, 20)
        """

        if self.metadata:
            return self.data.shape
        else:
            raise TypeError('Metadata for this file is not available, which suggests that file being analysed is not from one of the ISA imagers.')

    def centre(self):
        """Get the centre coordinate of image in earth coordinates
        Parameters
        ----------
        self: object
                Object of SatMap
        
        Returns
        -------
        tuple
            A tuple of two float numbers representing centre coordinate in earth coordinates
        Examples
        --------
        >>> if os.path.exists('aigean_lir_20221212_123848.asdf') != True: net.download_isa('aigean_lir_20221212_123848.asdf')
        >>> image = get_satmap('aigean_lir_20221212_123848.asdf')
        >>> image.centre()
        (300.0, 150.0)
        """

        if self.metadata:
            xcoords = self.metadata['xcoords']
            ycoords = self.metadata['ycoords']
            resolution = self.metadata['resolution']
            x_centre = xcoords[0] + (self.data.shape[1]/2)*resolution
            y_centre = ycoords[1] - (self.data.shape[0]/2)*resolution 
            centre_coor = (x_centre, y_centre)

            return centre_coor

        else:
            raise TypeError('Metadata for this file is not available, which suggests that file being analysed is not from one of the ISA imagers.')


    def __add__(self, other):

        """Add two SatMap object for the image on the same date and from the same instrument and return the result in format of SatMap 
        Parameters
        ----------
        self: object
                one of SatMap for adding
        
        other: object
                Another SatMap for adding
        Returns
        -------
        object
            A object in format of SatMap and storing information of adding result in metadata and data. 
        Examples
        --------
        >>> if os.path.exists('aigean_man_20230103_154956.hdf5') != True: net.download_isa("aigean_man_20230103_154956.hdf5")
        >>> if os.path.exists('aigean_man_20230103_161956.hdf5') != True: net.download_isa('aigean_man_20230103_161956.hdf5')
        >>> image1 = get_satmap('aigean_man_20230103_154956.hdf5')
        >>> image2 = get_satmap('aigean_man_20230103_161956.hdf5')
        >>> image_add = image1 + image2
        >>> image_add.metadata['xcoords']
        array([  0., 900.])
        >>> image_add.metadata['ycoords']
        array([  0., 400.])
        >>> image_add.data.shape
        (27, 60)
        >>> round(image_add.data[0, -2])
        225
        """
        if self.metadata and other.metadata:

            if self.metadata["instrument"] != other.metadata["instrument"]:
                raise TypeError('Two satmaps are not from the same instrument.')

            if self.metadata['date'] != other.metadata["date"]:
                raise TypeError('Two satmaps are not from the same day.')

            resolution = self.metadata['resolution']

            xcoords_self = self.metadata['xcoords']
            ycoords_self = self.metadata['ycoords']

            xcoords_other = other.metadata['xcoords']
            ycoords_other = other.metadata['ycoords']

            xcoords_add = [min(xcoords_self[0], xcoords_other[0]), max(xcoords_self[1], xcoords_other[1])]
            ycoords_add = [min(ycoords_self[0], ycoords_other[0]), max(ycoords_self[1], ycoords_other[1])]

            row = round((ycoords_add[1] - ycoords_add[0]) / resolution)
            col = round((xcoords_add[1] - xcoords_add[0]) / resolution)

            data_add = np.zeros((row, col))

            col_range_self = [round((xcoords_self[0]-xcoords_add[0])/resolution), round((xcoords_self[1]-xcoords_add[0])/resolution + 0.001)]
            row_range_self = [round((ycoords_add[1]-ycoords_self[1])/resolution), round((ycoords_add[1]-ycoords_self[0])/resolution + 0.001)]

            col_range_other = [round((xcoords_other[0]-xcoords_add[0])/resolution), round((xcoords_other[1]-xcoords_add[0])/resolution + 0.001)]
            row_range_other = [round((ycoords_add[1]-ycoords_other[1])/resolution), round((ycoords_add[1]-ycoords_other[0])/resolution + 0.001)]


            data_add[row_range_self[0]:row_range_self[1], col_range_self[0]:col_range_self[1]] = self.data
            data_add[row_range_other[0]:row_range_other[1], col_range_other[0]:col_range_other[1]] = other.data

            metadata_add = self.metadata.copy()
            metadata_add["xcoords"] = np.array(xcoords_add)
            metadata_add["ycoords"] = np.array(ycoords_add)

            time_add = self.metadata['time'] + "_and_" + other.metadata['time']
            metadata_add['time'] = time_add
            metadata_add['operation'] = 'add'

            return SatMap(data_add, metadata_add)

        else:
            raise TypeError('Metadata for this file is not available,which suggests that file being analysed is not from one of the ISA imagers.')


    def __sub__(self, other):

        """Subtract two SatMap object for the image on the different date and from the same instrument and return the result in format of SatMap 
        Parameters
        ----------
        self: object
                one of SatMap for subtracting
        
        other: object
                Another SatMap for subtracting
        Returns
        -------
        object
            A object in format of SatMap and storing information of subtracting result in metadata and data. 
        Examples
        --------
        >>> if os.path.exists('aigean_lir_20221223_024822.asdf') != True: net.download_isa("aigean_lir_20221223_024822.asdf")
        >>> if os.path.exists('aigean_lir_20230104_152610.asdf') != True: net.download_isa("aigean_lir_20230104_152610.asdf")
        >>> image1 = get_satmap('aigean_lir_20221223_024822.asdf')
        >>> image2 = get_satmap('aigean_lir_20230104_152610.asdf')
        >>> image_sub = image1 - image2
        >>> image_sub.metadata['xcoords']
        array([ 600., 1200.])
        >>> image_sub.metadata['ycoords']
        array([100., 300.])
        >>> image_sub.data.shape
        (7, 20)
        >>> round(image_sub.data[0, -3])
        -7
        """

        if self.metadata and other.metadata:
            if self.metadata["instrument"] != other.metadata["instrument"]:
                raise TypeError('Two satmaps are not from the same instrument.')

            if self.metadata['date'] == other.metadata["date"]:
                raise TypeError('Two satmaps are from the same day.')

            resolution = self.metadata['resolution']

            xcoords_self = self.metadata['xcoords']
            ycoords_self = self.metadata['ycoords']

            xcoords_other = other.metadata['xcoords']
            ycoords_other = other.metadata['ycoords']

            xcoords_subtract = [max(xcoords_self[0], xcoords_other[0]), min(xcoords_self[1], xcoords_other[1])]
            ycoords_subtract = [max(ycoords_self[0], ycoords_other[0]), min(ycoords_self[1], ycoords_other[1])]

            if xcoords_subtract[0] >= xcoords_subtract[1] or ycoords_subtract[0] >= ycoords_subtract[1]:
                raise TypeError('Two satmaps are non-overlapping.')

            row = round((ycoords_subtract[1] - ycoords_subtract[0]) / resolution)
            col = round((xcoords_subtract[1] - xcoords_subtract[0]) / resolution)

            data_subtract = np.zeros((row, col))

            col_range_self = [round((xcoords_subtract[0]-xcoords_self[0])/resolution), round((xcoords_subtract[1]-xcoords_self[0])/resolution + 0.001)]
            row_range_self = [round((ycoords_self[1]-ycoords_subtract[1])/resolution), round((ycoords_self[1]-ycoords_subtract[0])/resolution + 0.001)]

            col_range_other = [round((xcoords_subtract[0]-xcoords_other[0])/resolution), round((xcoords_subtract[1]-xcoords_other[0])/resolution + 0.001)]
            row_range_other = [round((ycoords_other[1]-ycoords_subtract[1])/resolution), round((ycoords_other[1]-ycoords_subtract[0])/resolution + 0.001)]

            data_subtract = self.data[row_range_self[0]:row_range_self[1], col_range_self[0]:col_range_self[1]]
            data_subtract = data_subtract - other.data[row_range_other[0]:row_range_other[1], col_range_other[0]:col_range_other[1]]

            metadata_subtract = self.metadata.copy()
            metadata_subtract["xcoords"] = np.array(xcoords_subtract)
            metadata_subtract["ycoords"] = np.array(ycoords_subtract)

            time = self.metadata['time'] + "_and_" + other.metadata['time']
            metadata_subtract['time'] = time
            metadata_subtract['operation'] = 'subtract'

            return SatMap(data_subtract, metadata_subtract)


        else:

            raise TypeError('Metadata for this file is not available,which suggests that file being analysed is not from one of the ISA imagers.')



    def mosaic(self, other, resolution = None, padding = True):

        """Add two SatMap object for the image on the same date and from the mixing instrument and return the result in format of SatMap 
        Parameters
        ----------
        self: object
                one of SatMap for adding
        
        other: object
                Another SatMap for adding
        resolution: int
                Resolution for the resultant image. If the resolution is not provided, it would be one of two satmaps with larger detail.
        padding: bool
                The default value of padding would be Ture and the return image would contain blanks. When padding is False, the resulant image 
                 would only cover the maximum portion without blanks.
        Returns
        -------
        object
            A object in format of SatMap and storing information of adding result in metadata and data.
             
        Examples
        --------
        >>> if os.path.exists('aigean_lir_20221223_024822.asdf') != True: net.download_isa("aigean_lir_20221223_024822.asdf")
        >>> if os.path.exists('aigean_man_20221223_030122.hdf5') != True: net.download_isa("aigean_man_20221223_030122.hdf5")
        >>> image1 = get_satmap('aigean_lir_20221223_024822.asdf')
        >>> image2 = get_satmap('aigean_man_20221223_030122.hdf5')
        >>> image_mosaic = image1.mosaic(image2)
        >>> image_mosaic.metadata['xcoords']
        array([ 600., 1500.])
        >>> image_mosaic.metadata["ycoords"]
        array([100., 500.])
        >>> image_mosaic.data.shape
        (27, 60)
        >>> round(image_mosaic.data[1, -1])
        327
        """

        if self.metadata and other.metadata:

            if resolution != None and type(resolution) != int:
                raise TypeError('The resolution must be an integer.')

            if resolution != None and resolution <= 0:
                raise ValueError('The resolution must be positive')

            if type(padding) != bool:
                raise TypeError('The padding must be True or False')

            if self.metadata['date'] != other.metadata["date"]:
                raise TypeError('Two satmaps are not from the same day.')

            if resolution == None:
                if self.metadata['resolution'] <= other.metadata['resolution']:
                    resolution = self.metadata['resolution']
                else:
                    resolution = other.metadata['resolution']

            xcoords_self = self.metadata['xcoords']
            ycoords_self = self.metadata['ycoords']

            xcoords_other = other.metadata['xcoords']
            ycoords_other = other.metadata['ycoords']

            if resolution >= (ycoords_self[1] - ycoords_self[0]) or resolution >= (xcoords_self[1] - xcoords_self[0]) or resolution >= (ycoords_other[1] - ycoords_other[0]) or resolution >= (xcoords_other[1] - xcoords_other[0]):
                raise ValueError('Resolution is too large.')

            #rescale images
            if self.metadata['resolution'] != resolution:
                if self.metadata['resolution'] > resolution:
                    self_scale = self.metadata['resolution']/resolution
                    self_data_rescale = rescale(self.data, self_scale, order=3, mode = 'edge')
                else:
                    self_scale = round(resolution/self.metadata['resolution'])
                    self_data_rescale = downscale_local_mean(self.data, (self_scale, self_scale) )
                    print(self_data_rescale.shape)
            else:
                self_data_rescale = self.data[:]

            if other.metadata['resolution'] != resolution:
                if other.metadata['resolution'] > resolution:
                    other_scale = other.metadata['resolution']/resolution
                    other_data_rescale = rescale(other.data, other_scale, order=3, mode = 'edge')
                else:
                    other_scale = round(resolution/other.metadata['resolution'])
                    other_data_rescale = downscale_local_mean(other.data, (other_scale, other_scale) )
            else:
                other_data_rescale = other.data[:]

            #get the image after adding
            xcoords_add = [min(xcoords_self[0], xcoords_other[0]), max(xcoords_self[1], xcoords_other[1])]
            ycoords_add = [min(ycoords_self[0], ycoords_other[0]), max(ycoords_self[1], ycoords_other[1])]

            row = round((ycoords_add[1] - ycoords_add[0]) / resolution)
            col = round((xcoords_add[1] - xcoords_add[0]) / resolution)

            data_add = np.zeros((row, col))

            col_range_self = [round((xcoords_self[0]-xcoords_add[0])/resolution), round((xcoords_self[1]-xcoords_add[0])/resolution + 0.001)]
            row_range_self = [round((ycoords_add[1]-ycoords_self[1])/resolution), round((ycoords_add[1]-ycoords_self[0])/resolution + 0.001)]


            col_range_other = [round((xcoords_other[0]-xcoords_add[0])/resolution), round((xcoords_other[1]-xcoords_add[0])/resolution + 0.001)]
            row_range_other = [round((ycoords_add[1]-ycoords_other[1])/resolution), round((ycoords_add[1]-ycoords_other[0])/resolution + 0.001)]


            row_self_reshape = row_range_self[1] - row_range_self[0]
            col_self_reshape = col_range_self[1] - col_range_self[0]
            row_other_reshape = row_range_other[1] - row_range_other[0]
            col_other_reshape = col_range_other[1] - col_range_other[0]
            data_add[row_range_self[0]:row_range_self[1], col_range_self[0]:col_range_self[1]] = self_data_rescale[0:row_self_reshape, 0:col_self_reshape]
            data_add[row_range_other[0]:row_range_other[1], col_range_other[0]:col_range_other[1]] = other_data_rescale[0:row_other_reshape, 0:col_other_reshape]

            if padding == True:

                metadata_add = {}

                metadata_add["observatory"] = self.metadata["observatory"]

                instrument = self.metadata['instrument']
                metadata_add["instrument"] = instrument

                metadata_add["xcoords"] = np.array(xcoords_add)
                metadata_add["ycoords"] = np.array(ycoords_add)

                metadata_add['resolution'] = resolution

                metadata_add["date"] = self.metadata["date"]

                time_add = self.metadata['time']
                metadata_add['time'] = time_add
                metadata_add['operation'] = 'mosaic'

                return SatMap(data_add, metadata_add)

            else:
                #without padding
                
                # find the overlapping area
                xcoords_overlap = [max(xcoords_self[0], xcoords_other[0]), min(xcoords_self[1], xcoords_other[1])]
                ycoords_overlap = [max(ycoords_self[0], ycoords_other[0]), min(ycoords_self[1], ycoords_other[1])]


                if xcoords_overlap[0] >= xcoords_overlap[1] or ycoords_overlap[0] >= ycoords_overlap[1]:
                    row_overlap = 0
                    col_overlap = 0
                    col_range_overlap = [0,0]
                    row_range_overlap = [0,0]
                else:
                    row_overlap = round((ycoords_overlap[1] - ycoords_overlap[0]) / resolution)
                    col_overlap = round((xcoords_overlap[1] - xcoords_overlap[0]) / resolution)
                    col_range_overlap = [round((xcoords_overlap[0]-xcoords_add[0])/resolution), round((xcoords_overlap[1]-xcoords_add[0])/resolution + 0.001)]
                    row_range_overlap = [round((ycoords_add[1]-ycoords_overlap[1])/resolution), round((ycoords_add[1]-ycoords_overlap[0])/resolution + 0.001)]

                #comparing areas of different part

                area1 = row_overlap*col
                area2 = col_overlap*row
                area3 = self_data_rescale.shape[0]*self_data_rescale.shape[1]
                area4 = other_data_rescale.shape[0]*other_data_rescale.shape[1]

                maximum_area = 0
                col_range_nonpad = []
                row_range_nonpad = []
                xcoords_nonpad = []
                ycoords_nonpad = []

                if maximum_area <= area1:
                    maximum_area = area1
                    col_range_nonpad = [0, col]
                    row_range_nonpad = row_range_overlap[:]
                    xcoords_nonpad = xcoords_add[:]
                    ycoords_nonpad = ycoords_overlap[:]

                    if maximum_area <= area2:
                        maximum_area = area2
                        col_range_nonpad = col_range_overlap[:]
                        row_range_nonpad = [0, row]
                        xcoords_nonpad = xcoords_overlap[:]
                        ycoords_nonpad = ycoords_add[:]

                        if maximum_area <= area3:
                            maximum_area = area3
                            col_range_nonpad = col_range_self[:]
                            row_range_nonpad = row_range_self[:]
                            xcoords_nonpad = xcoords_self[:]
                            ycoords_nonpad = ycoords_self[:]

                            if maximum_area <= area4:
                                maximum_area = area4
                                col_range_nonpad = col_range_other[:]
                                row_range_nonpad = row_range_other[:]
                                xcoords_nonpad = xcoords_other[:]
                                ycoords_nonpad = ycoords_other[:]

                row_nonpad = row_range_nonpad[1]-row_range_nonpad[0]
                col_nonpad = col_range_nonpad[1] - col_range_nonpad[0]
                data_nonpad = np.zeros((row_nonpad, col_nonpad))
                data_nonpad = data_add[row_range_nonpad[0]:row_range_nonpad[1], col_range_nonpad[0]:col_range_nonpad[1]]

                metadata_nonpad = {}
                metadata_nonpad["observatory"] = self.metadata["observatory"]

                instrument = self.metadata['instrument']
                metadata_nonpad["instrument"] = instrument

                metadata_nonpad["xcoords"] = np.array(xcoords_nonpad)
                metadata_nonpad["ycoords"] = np.array(ycoords_nonpad)

                metadata_nonpad['resolution'] = resolution

                metadata_nonpad["date"] = self.metadata["date"]

                time_add = self.metadata['time'] 
                metadata_nonpad['time'] = time_add
                metadata_nonpad['operation'] = 'mosaic'

                return SatMap(data_nonpad, metadata_nonpad)

    

    def visualize(self, save = False, savepath = None):

        """Fuction for displaying or saving the image 
        Parameters
        ----------
        self: class
                class of SatMap
        
        save: bool
                The default value of save is False and the image would display. If save is True, the image 
                would not display and save the image in the required path.
        savepath: str
                The default value of savepath is None and the file would storge in the current directory, if savepath
                is not provided.
 
        Examples
        --------
        >>> if os.path.exists('aigean_lir_20221223_024822.asdf') != True: net.download_isa("aigean_lir_20221223_024822.asdf")
        >>> image = get_satmap('aigean_lir_20221223_024822.asdf')
        >>> image.visualize(save = True)
        >>> Path('Aigean_Lir_20221223_024822.png').exists()
        True
        """


        if type(save) != bool:
            raise TypeError('The type of save should be bool, such as True and Flase')
        
        if type(savepath) != str and savepath != None:
            raise TypeError('The type of savepath should be string.')

        x_len = int(self.data.shape[1])
        y_len = int(self.data.shape[0])
        x_ticks = np.arange(x_len)
        y_ticks = np.arange(y_len)

        resolution = self.metadata['resolution']

        x_labels = np.arange(self.metadata['xcoords'][0] + resolution/2, self.metadata['xcoords'][1], self.metadata['resolution'])
        y_labels = np.arange(self.metadata['ycoords'][1] - resolution/2 , self.metadata['ycoords'][0], -(self.metadata['resolution']))

        if 'operation' in self.metadata and self.metadata['operation'] == "subtract":
            plt.imshow(self.data, cmap = "PRGn" )
        else:
            plt.imshow(self.data )
        plt.tick_params(axis='both', labelsize=7)
        plt.xticks(x_ticks, x_labels)
        plt.xticks(rotation=90, fontsize=7)
        plt.yticks(y_ticks, y_labels)

        if save == False:
            plt.show()

        else:
            if 'operation' in self.metadata:
                filename = self.metadata["observatory"] + "_" + self.metadata["instrument"] + "_" +self.metadata["date"] + "_" + self.metadata["time"] + "_" + self.metadata["operation"]+ ".png"
            else:
                filename = self.metadata["observatory"] + "_" + self.metadata["instrument"] + "_" +self.metadata["date"] + "_" + self.metadata["time"] + ".png"
            filename = filename.replace('-', "")
            filename = filename.replace(':', "")

            if savepath == None:
                plt.savefig(filename)
            else:
                pathname = savepath + filename
                plt.savefig(pathname)



