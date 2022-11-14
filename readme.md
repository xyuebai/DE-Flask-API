# Utopia Candidate Test Project
## Project Descscription

This project contains 2 parts, the first part is data preprocessing and the second part is a flask API. Data preprocessing read CSV files run data transformation and analytics and finally saves the result in CSV files. Flask API provides endpoints to the preprocessed data

## Prerequest
- Python==3.9.7

 ## File structure
 
    .
    ├── data_transformation                   # Task I & II
    │   ├── src
    │   │   ├── __init.py__     
    │   │   ├── data_toolkit.py             # Apply data transformation
    │   │   └── transformation.py            # Data transformation entry
    │   ├── test
    │   │   └── test_transfromation.py            # Unit test
    │   └── data_exploration.ipynb              # Data exploration with Jupyter Notebook
    ├── flask_api
    │   ├── app
    │   │   ├── app.py            # api entry point
    │   │   └── resrouces  
    │   │       ├── __init__.py
    │   │       └── resrouce.py         # api endpoints
    │   └── test       
    ├── output      # output folder to save the result
    ├── log      # output folder to save the log
    ├── .gitignore 
    ├── requirements.txt 
    └── readme.md


## How to run
```
$ cd <git-repo-dir>      # project root directory
$ python3 -m venv <venv-name>
$ source <venv-name>/bin/activate
$ pip install -r requirements.txt
```

### 1. Data Preprocessing
```
$ export PYTHONPATH="{PYTHONPATH}:<git-repo-dir>/data_transformation"
$ cd data_transformation/src        # from root directory 
$ python transformation.py      # run data transformation 
```

### 1. Data Preprocessing - Unit Test
```
$ export PYTHONPATH="{PYTHONPATH}:<git-repo-dir>/data_transformation"
$ cd data_transformation/test        # from root directory 
$ python test_transformation.py     # run unit test 
```

### 2. Flask API
```
$ cd flask_api/app       # from root directory
$ python app.py       # start flask api service

```
## API Definition

Route  | Verb | info
---------|----------|---------
 max_value | GET | return the value set in variable NORMALIZATION_MAX
 playlist/<playlist_id> | GET | display all elements of the playlist specified by playlist_id, if playlist_id doesn't exist, return 404
 tracklist/<playlist_id> | GET | return a list of track_ids associated with the playlist, if playlist_id doesn't exist, return 404

## API Example endpoint

### 1. Query max_value
`curl http://localhost:5050/max_value`
### 1. Query playlists
`curl http://localhost:5050/playlist/<playlist_id>`
### 1. Query tracklists
`curl http://localhost:5050/tracklist/<playlist_id>`




