from setuptools import setup, find_packages

VERSION = '0.1.1' 
DESCRIPTION = 'A python package for interacting with wyze camera video data.'
LONG_DESCRIPTION = '...'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="wyzepy", 
        version=VERSION,
        author="Fausto Lopez",
        author_email="<youremail@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["moviepy"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)