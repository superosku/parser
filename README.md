
## About

This simple script matches doctor data from `match_file.csv` to the doctor data in `source_data.json`.

Two doctors are a match when

 - They have the same npi **or**.
 - If one of them is missing the npi information, they have the same name and the same address.

If these conditions are not met, two doctors are not counted as a match. Reasoning for this is:

 - If two entries have the same npi, they most certainly refer to the same doctor.
 - We can not trust that the entries refer to the same doctor if their only similarity is the name. It is too common to have same names.
 - Two entries with the same name and address but different npi can not refer to the same doctor.

The script is made with python3. Instructions for setting it up, running unit tests and running the script can be found below.

Instructions should work at least on mac os x.

The script takes around 9 seconds to run on my machine. I assumed that performance was not critical for this task.

## Installing

Set up a virtual environment. You might need to install virtualenvwrapper first: `sudo pip install virtualenvwrapper`
```
mkvirtualenv doctor --python=`which python3`
echo "workon doctor" > .env
```

Install requirements
```
pip install -r requirements.txt
```

## Running tests

Run unit tests
```
py.test
```

Run linters
```
flake8 .
```
and
```
isort --recursive --diff .
```

## Running the script

```
python main.py
```
