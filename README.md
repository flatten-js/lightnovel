# Lightnovel

Automatically generate light novel-style titles from existing light novel titles using Markov chains and other techniques.

## Get Started
The first step is to clone the git repository
```
$ git clone https://github.com/flatten-js/lightnovel.git
```

### Requirement

#### MeCab
Open Source Morphological Analysis Engine

##### Homebrew

Install the unit and dictionary
```
$ brew install mecab mecab-ipadic
```

For use in a python
```
$ pip install mecab-python3
```

## Usage

### Launch
Launch a python without specifying a file
```
$ python
```

### Initialization
Initialization process including instantiation of the novelizer class
```
>>> import lightnovel
>>> novel = lightnovel.Novelizer()
```

### Novelizer specifications

#### Registration
Register the text that will be the morpheme model
```
>>> novel.register(file, text)

    Parameters
    ----------
    file : str, default "title.txt"
       Register text from text file
    text : str, default ""
       Register text directly without going through a text file

    Notes
    -----
    Parameter priority : text < file
```

#### Inspection
Validate the formed morpheme model
```
>>> novel.inspect()
```

#### Build
Materialize morpheme model as DB
```
>>> novel.build()
```

#### Generation
Generate novel based on materialized morpheme model
```
>>> novel.novelize(n)

    Parameters
    ----------
    n : int, default 1
        Number of novels to generate
```
