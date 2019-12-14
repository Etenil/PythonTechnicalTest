# Origin Markets Backend Test

## Project Quickstart

Inside a virtual environment running Python 3:
- `pip install -r requirement.txt`
- `./manage.py migrate` to get the DB ready
- `./manage.py createsuperuser` to create a super-user
- `./manage.py runserver` to run server.
- `./manage.py test` to run tests.

## What works
The entire exercise is functional:

- adding bonds
- listing bonds
- authentication (I chose Basic for simplicity)
- bond ownership and active-user filtering of bonds
- retrieving the legal name from the LEI


## Stuff I could improve

- A known LEI is not queried again, so the legal names table could get outdated
- The LEI isn't validated, it's a standard format so that should be doable but
    I couldn't find a ready-made validator or parser for it
- There must be a better way to handle the user and legal_name sub-serializers in
    the BondSerializer; however I'm not sufficiently familiar with DRF to figure
    it out yet (I use mostly Flask). I find DRF very good though
