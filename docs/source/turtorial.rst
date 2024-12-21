Turtorial Section
=================

Here would represent a small turtorial, which includes an example of query and download images for a particular date

Once you install the package, you should first use query_isa function to obtain results from the ISA data archive query 
service as JSON files and returns the url of the query. Suppose you want to query the data on 20221222 for Fand, 

.. code-block:: 

    $ from aigeanpy.net import query_isa
    $ lir_map = query_isa(start_date='2022-12-22', stop_date='2022-12-22', instrument = 'Fand')

Then, you could download the file according to the filenames for different time. For example,

.. code-block:: 

    $ from aigeanpy.net import download_isa
    $ lir_map = download_isa('aigean_fan_20221222_031108.zip')

Finally, you could obtain the images using get_satmap() function, 

.. code-block:: 
    
    $ from aigeanpy.satmap import get_satmap
    $ image = get_satmap('aigean_fan_20221222_031108')
