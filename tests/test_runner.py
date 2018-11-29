import os, sys
import yaml
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firebaserunner.runner import *

config = yaml.load(open('./config.yml'))['firebase']

def test_set_app_apk_path():
    runner = Runner(config['service-key'], 'project', True)
    runner.set_app_apk_path('test')
    assert runner.api_body['testSpecification']['androidInstrumentationTest']['appApk']['gcsPath'] == 'test'
    
def test_set_test_apk_path():
    runner = Runner(config['service-key'], 'project', True)
    runner.set_test_apk_path('test')
    assert runner.api_body['testSpecification']['androidInstrumentationTest']['testApk']['gcsPath'] == 'test'

def test_set_device():
    device = {
        'model': 'test',
        'version': '1'
    }
    expected = {'androidModelId': 'test', 'androidVersionId': '1', 'locale': 'en', 'orientation': 'portrait'}
    runner = Runner(config['service-key'], 'project', True)
    runner.set_device(device)
    assert runner.api_body['environmentMatrix']['androidDeviceList']['androidDevices'] == [expected]

def test_set_result_storage_path():
    runner = Runner(config['service-key'], 'project', True)
    runner.set_result_storage_path('test')
    assert runner.api_body['resultStorage']['googleCloudStorage']['gcsPath'] == 'test'
