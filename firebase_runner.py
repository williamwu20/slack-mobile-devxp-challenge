from firebaserunner.runner import *
from firebaserunner.logger import setup_logger
from halo import Halo

import polling
import time
import logging

# Setup logger
logger = logging.getLogger(__name__)
setup_logger(logger)

def main():
    # Instantiate runner instance
    runner = Runner()

    # Upload app-apk to GCS
    logger.info('Uploading app apk..')
    runner.upload('./apk/app-debug.apk', 'app-debug.apk')

    # Upload test apk
    logger.info('Uploading app test apk..')
    runner.upload('./apk/app-debug-androidTest.apk', 'app-debug-androidTest.apk')

    # Set paths and environment
    runner.set_app_apk_path()
    runner.set_test_apk_path()
    runner.set_environment()
    runner.set_result_storage_path()

    # Execute run
    logger.info('Executing run...')
    test_run = runner.run_test()

    # Polling for test run completion (not good - but unfortunately FTL has no webhook to trigger when run is complete)
    with Halo(text='Test running: ' + test_run['testMatrixId'] + ' on Firebase Test Lab (approx 10 min)', spinner='line'):
        polling.poll(
            lambda: runner.get_test_run(test_run['testMatrixId']).get('state') == 'FINISHED',
            step=30,
            poll_forever=True
        )
    
    # Download and parse test results
    logger.info('Downloading test results into /test_result..')
    runner.download('test_results/NexusLowRes-28-en-portrait/test_result_1.xml', './test_result/test_result_1.xml')
    logger.info('Run complete!')

if __name__ == "__main__":
   main()


