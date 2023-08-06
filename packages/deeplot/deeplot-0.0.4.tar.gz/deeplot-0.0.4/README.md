# deeplot
a library to display/visualize images of neural networks
![PyTorch Tabular](deeplot_logo.png)    

[![pypi](https://img.shields.io/pypi/v/pytorch_tabular.svg)](https://pypi.python.org/pypi/deeplot)
![PyPI - Downloads](https://img.shields.io/pypi/dm/deeplot)
[![DOI](https://zenodo.org/badge/321584367.svg)](https://zenodo.org/badge/latestdoi/321584367)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square)](https://github.com/SimeraAI/deeplot/issues)

Python Library aimed for displaying architecture image of neural networks.

*Low code

*Easy to use

This library has been built using opencv and matplotlib.

## Table of Contents

- [Installation](#installation)
- [Documentation](#documentation)
- [Available Architectures](#available-models)
- [Usage](#usage)


## Installation

Create a python virtual environment using venv or conda or pipenv etc.
Once, you have the env ready, just use below command to get the installation going:
```
 pip install -m deeplot
```

The sources for deeplot can be downloaded from the `Github repo`_.

You can either clone the public repository:

```
git clone https://github.com/SimeraAI/deeplot.git
```

Once you have a copy of the source, you can install it with:

```
python setup.py install
```

## Documentation

For complete Documentation with tutorials visit [ReadTheDocs](https://pytorch-tabular.readthedocs.io/en/latest/ )

## Available Architectures

* [ResNet](#resnet)
* [DenseNet](#densenet)
* [VGG](#vgg)
* [MobileNet](#mobilenet)
* [SqueezeNet](#squeezenet)
* [Inception](#inception)
* [ResNeXt](#resnext)


## Usage
```python
from deeplot import deeplot

deeplot.VGG()
deeplot.GoogleNet()
```

## Future Roadmap(Contributions are Welcome)
Add new Architectures
include a visualization of the architecture
include a util tool to convert the architecture to a graph


        


