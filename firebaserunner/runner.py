from google.oauth2 import service_account
from google.cloud import storage
import googleapiclient.discovery
import json

class Runner:

    BUCKET_ID = 'mobile-devxp-coding-exercise.appspot.com'
    PRIVATE_KEY_PATH = './firebaserunner/private_key.json'
    ROOT_STORAGE_PATH = 'gs://' + BUCKET_ID
    DEFAULT_STORAGE_PATH = ROOT_STORAGE_PATH + '/test_results/'
    DEFAULT_APP_APK_PATH = ROOT_STORAGE_PATH + '/app-debug.apk'
    DEFAULT_TEST_APK_PATH = ROOT_STORAGE_PATH + '/app-debug-androidTest.apk'
    PROJECT_ID = 'mobile-devxp-coding-exercise'
    ENVIRONMENT_DEFAULT = {
        'androidModelId': 'NexusLowRes',
        'androidVersionId': '28',
        'locale': 'en',
        'orientation': 'portrait'
    }

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(self.PRIVATE_KEY_PATH)
        self.client=googleapiclient.discovery.build('testing', 'v1', credentials=credentials)
        self.storage_client = storage.Client(self.PROJECT_ID, credentials=credentials)
        self.api_body = {
            'testSpecification': {
                'androidInstrumentationTest': {
                    'appApk': {
                        'gcsPath': ''
                    },
                    'testApk': {
                        'gcsPath': ''
                    }
                },
                'disableVideoRecording': True
            },
            'environmentMatrix': {
                'androidDeviceList': {
                    'androidDevices': []
                }
            },
            'resultStorage': {
                'googleCloudStorage': {
                    'gcsPath': ''
                }
            }
        }

    def run_test(self):
        return self.client.projects().testMatrices().create(projectId=self.PROJECT_ID, body=self.api_body).execute()
    
    def get_test_run(self, test_matrix_id):
        return self.client.projects().testMatrices().get(projectId=self.PROJECT_ID, testMatrixId=test_matrix_id).execute()

    def set_app_apk_path(self, app_apk_path=DEFAULT_APP_APK_PATH):
        self.api_body['testSpecification']['androidInstrumentationTest']['appApk']['gcsPath'] = app_apk_path
    
    def set_test_apk_path(self, test_apk_path=DEFAULT_TEST_APK_PATH):
        self.api_body['testSpecification']['androidInstrumentationTest']['testApk']['gcsPath'] = test_apk_path

    def set_environment(self, environment=ENVIRONMENT_DEFAULT):
        self.api_body['environmentMatrix']['androidDeviceList']['androidDevices'] = [environment]

    def set_result_storage_path(self, result_storage_path=DEFAULT_STORAGE_PATH):
        self.api_body['resultStorage']['googleCloudStorage']['gcsPath'] = result_storage_path

    def download(self, source_name, destination_name):
        bucket = self.storage_client.get_bucket(self.BUCKET_ID)
        blob = bucket.blob(source_name)
        blob.download_to_filename(destination_name)

    def upload(self, source_name, destination_name):
        bucket = self.storage_client.get_bucket(self.BUCKET_ID)
        blob = bucket.blob(destination_name)
        blob.upload_from_filename(source_name)