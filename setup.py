from setuptools import setup, find_packages


setup(
    name="aigeanpy",
    version="1.0.0",
    packages=find_packages(exclude=["test_*","*.test.","test"]),
    url = 'https://github.com/UCL-COMP0233-22-23/aigeanpy-Working-Group-10.git',
    author = 'Chenghao Li, Joe Lee, Maruf Talukdar, Simian Xing',
    description = 'The package of aigean',
    install_requires = ['argparse',
                        'requests', 
                        'pathlib',
                        'asdf',
                        'h5py',
                        'numpy',
                        'matplotlib',
                        'scikit-image'],
    entry_points={
        'console_scripts': [
            'aigean_today = aigeanpy.aigean_today:cli',
            'aigean_metadata = aigeanpy.aigean_metadata:cli',
            'aigean_mosaic = aigeanpy.aigean_mosaic:cli'
        ]} 

    )
