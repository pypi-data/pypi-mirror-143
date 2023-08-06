from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'sketchpy mobile version'
LONG_DESCRIPTION = 'A package to do sketching animation with many built in functions, a library is also availabe where you can play with different pre defined sketches, you can also create your own sketch and do the animation yourself'

# Setting up
setup(
    name="sketchpy-mob",
    version=VERSION,
    author="Mr Mystery",
    author_email="sriramanand23@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['turtle==0.0.1', 'wheel','svg.path','svgpathtools','tqdm'],
    keywords=['python', 'sketch', 'drawing', 'animation', 'code hub', 'pencil sketch', 'painting'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)