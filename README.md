# Slack Mobile DevXP Challenge

## Installation
Can use Python 2.7+

Recommend using virtualenv
```
virtualenv env 
source env/bin/activate
pip install -r requirements.txt
```
## Firebase Test Lab
- Create free spark account and a project at https://console.firebase.google.com/u/0/project/_/overview?purchaseBillingPlan=free

## Authentication
- Go to https://console.developers.google.com/apis/credentials
- With your FTL project selected, select Create credentials dropdown and select Service account key
- Choose service account and download as JSON

## Configuration
Modify `config.yml` to fit your project and run needs

```yaml
# https://cloud.google.com/sdk/gcloud/reference/firebase/test/android/run
firebase:
  bucket: your-project.appspot.com
  results-bucket: /test_results/
  record-video: false
  project: your-project-id

  # Paths to app and test apk and test result output directory
  app: /path/to/app/apk
  test: /path/to/test/apk
  output: ./test_result

  # Path to service account key txt
  service-key: /path/to/service/key.txt
  
  device:
      model: NexusLowRes
      version: '28'
```

## Usage
```
python firebase_runner.py
```
