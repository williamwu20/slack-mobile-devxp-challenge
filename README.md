# Slack Mobile DevXP Challenge

## Installation
Requires Python 2.7+

```
virtualenv env 
source env/bin/activate
pip install -r requirements.txt
```
## Authentication
- Go to https://console.developers.google.com/apis/credentials and login as a user with access to `mobile-devxp-coding-exercise` project
- With `mobile-devxp-coding-exercise project` selected, select Create credentials dropdown and select Service account key
- Choose or create service account and download as JSON
- Rename JSON to `private_key.json` and move to `/firebaserunner` directory

## Usage
```
python firebase_runner.py
```
