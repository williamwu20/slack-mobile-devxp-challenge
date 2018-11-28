from google.oauth2 import service_account
from google.cloud import storage

import googleapiclient.discovery

class Runner:

    def __init__(self, config):
        self.config = config
        credentials = service_account.Credentials.from_service_account_file(config['service-key'])
        self.client = googleapiclient.discovery.build('testing', 'v1', credentials=credentials)
        self.storage_client = storage.Client(config['project'], credentials=credentials)
        self.environment = {
            'androidModelId': config['device']['model'],
            'androidVersionId': config['device']['version'],
            'locale': 'en',
            'orientation': 'portrait'
        }
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
                'disableVideoRecording': config['record-video']
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
        return self.client.projects() \
            .testMatrices() \
            .create(projectId=self.config['project'], body=self.api_body) \
            .execute()
    
    def get_test_run(self, test_matrix_id):
        return self.client.projects() \
            .testMatrices() \
            .get(projectId=self.config['project'], testMatrixId=test_matrix_id) \
            .execute()

    def set_app_apk_path(self, app_apk_path=''):
        self.api_body['testSpecification']['androidInstrumentationTest']['appApk']['gcsPath'] = app_apk_path
    
    def set_test_apk_path(self, test_apk_path=''):
        self.api_body['testSpecification']['androidInstrumentationTest']['testApk']['gcsPath'] = test_apk_path

    def set_environment(self):
        self.api_body['environmentMatrix']['androidDeviceList']['androidDevices'] = [self.environment]

    def set_result_storage_path(self, result_storage_path=''):
        self.api_body['resultStorage']['googleCloudStorage']['gcsPath'] = result_storage_path

    def download(self, source_name, destination_name):
        bucket = self.storage_client.get_bucket(self.config['bucket'])
        blob = bucket.blob(source_name)
        blob.download_to_filename(destination_name)

    def upload(self, source_name, destination_name):
        bucket = self.storage_client.get_bucket(self.config['bucket'])
        blob = bucket.blob(destination_name)
        blob.upload_from_filename(source_name)