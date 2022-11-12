# Utopia Candidate Test Project
## Project Descscription

This project contains 2 parts, frist part is data preprocessing and the second part is flask api. Let's have a look of the repository dictionary arrangment

## Prerequest
- Python==3.9.7

 ## File structure
 
    .
    ├── data_transformation                   # Task I & II
    │   ├── __init.py__             
    │   ├── data_exploration.ipynb              # Data exploration with Jupyter Notebook
    │   ├── test_transformation.py             # Unit test for methods
    │   └── transformation.py            # Data transformation for task I & II
    ├── flask_api
    │   ├── app
    │   │   ├── app.py            # api entry point
    │   │   └── resrouces  
    │   │       ├── __init__.py
    │   │       └── resrouce.py         # api endpoints
    │   └── test       
    ├── output      # output folder to save the result
    ├── .gitignore 
    ├── requirements.txt 
    └── readme.md


## How to run
```
$ cd utopia_interview       # project root directory
$ python3 -m venv <venv-name>
$ source <venv-name>/bin/activate
$ pip install -r requirements.txt
```

### 1. Data Preprocessing
```
$ cd data_transformation        # from root directory 
$ python transformation.py      # run data transformation 
$ python test_transformation.py     # run unit test 
```

### 2. Flask API
```
$ cd flask_api/app       # from root directory
$ python app.py       # run flask api

```
## API Definition

Route  | Verb | info
---------|----------|---------
 max_value | GET | return the value set in variable NORMALIZATION_MAX
 playlist/<playlist_id> | GET | display all elements of the playlist specified by playlist_id
 tracklist/<playlist_id> | GET | return a list of track_ids associated with the playlist 

## API Example endpoint

### 1. Query max_value
`curl http://localhost:5050/max_value`
### 1. Query max_value
`curl http://localhost:5050/playlist/<playlist_id>`
### 1. Query max_value
`curl http://localhost:5050/tracklist/<playlist_id>`




