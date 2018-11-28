import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firebaserunner.runner import *

def test_set_app_apk_path():
    runner = Runner()
    runner.set_app_apk_path('test')
    assert runner.api_body['testSpecification']['androidInstrumentationTest']['appApk']['gcsPath'] == 'test'
    
def test_set_test_apk_path():
    runner = Runner()
    runner.set_test_apk_path('test')
    assert runner.api_body['testSpecification']['androidInstrumentationTest']['testApk']['gcsPath'] == 'test'

def test_set_environment():
    runner = Runner()
    runner.set_environment('test')
    assert runner.api_body['environmentMatrix']['androidDeviceList']['androidDevices'] == ['test']

def test_set_result_storage_path():
    runner = Runner()
    runner.set_result_storage_path('test')
    assert runner.api_body['resultStorage']['googleCloudStorage']['gcsPath'] == 'test'
