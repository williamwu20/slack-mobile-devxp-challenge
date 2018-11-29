from google.oauth2 import service_account
from google.cloud import storage

import googleapiclient.discovery

class Runner:

    def __init__(self, service_key, project, record_video):
        credentials = service_account.Credentials.from_service_account_file(service_key)
        self.project = project
        self.client = googleapiclient.discovery.build('testing', 'v1', credentials=credentials)
        self.storage_client = storage.Client(project, credentials=credentials)
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
                'disableVideoRecording': record_video
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
            .create(projectId=self.project, body=self.api_body) \
            .execute()
    
    def get_test_run(self, test_matrix_id):
        return self.client.projects() \
            .testMatrices() \
            .get(projectId=self.project, testMatrixId=test_matrix_id) \
            .execute()

    def set_app_apk_path(self, app_apk_path=''):
        self.api_body['testSpecification']['androidInstrumentationTest']['appApk']['gcsPath'] = app_apk_path
    
    def set_test_apk_path(self, test_apk_path=''):
        self.api_body['testSpecification']['androidInstrumentationTest']['testApk']['gcsPath'] = test_apk_path

    def set_device(self, device_config={}):
        device = {
            'androidModelId': device_config['model'],
            'androidVersionId': device_config['version'],
            'locale': 'en',
            'orientation': 'portrait'
        }
        self.api_body['environmentMatrix']['androidDeviceList']['androidDevices'].append(device)

    def set_result_storage_path(self, result_storage_path=''):
        self.api_body['resultStorage']['googleCloudStorage']['gcsPath'] = result_storage_path

    def download(self, bucket, source_name, destination_name):
        bucket = self.storage_client.get_bucket(bucket)
        blob = bucket.blob(source_name)
        blob.download_to_filename(destination_name)

    def upload(self, bucket, source_name, destination_name):
        bucket = self.storage_client.get_bucket(bucket)
        blob = bucket.blob(destination_name)
        blob.upload_from_filename(source_name)