from firebaserunner.runner import Runner
from firebaserunner.logger import setup_logger
from halo import Halo

import time
import logging
import yaml

config = yaml.load(open('./config.yml'))['firebase']

# Setup logger
logger = logging.getLogger(__name__)
setup_logger(logger)

def main():
    # Instantiate runner instance
    runner = Runner(config)
    apk_path = 'gs://{}'.format(config['bucket'])

    # Upload app-apk to GCS
    logger.info('Uploading app apk..')
    runner.upload(config['app'], 'app-debug.apk')

    # Upload test apk
    logger.info('Uploading app test apk..')
    runner.upload(config['test'], 'app-debug-androidTest.apk')

    # Set paths and environment
    runner.set_app_apk_path(app_apk_path='{}/app-debug.apk'.format(apk_path))
    runner.set_test_apk_path(test_apk_path='{}/app-debug-androidTest.apk'.format(apk_path))
    runner.set_environment()
    runner.set_result_storage_path(result_storage_path='gs://{}/{}'.format(config['bucket'], config['results-bucket']))

    # Execute run
    logger.info('Executing run...')
    test_run = runner.run_test()
    
    # Initial test state and progress message
    test_state = runner.get_test_run(test_run['testMatrixId'])['state']
    progress_message = ''
    spinner = Halo(spinner='line')

    # Poll matrix (sadly I did not find a webhook for FTL - this can also be optimized with async I/O)
    logger.info('Polling {} ..'.format(test_run['testMatrixId']))
    spinner.start()

    while test_state != 'FINISHED':
        test = runner.get_test_run(test_run['testMatrixId'])
        current_state = test['state']
        if test_state == 'INVALID' or test_state == 'ERROR':
            if 'testDetails' in test['testExecutions'][0]:
                error_message = test['testExecutions'][0]['testDetails']['errorMessage']
                spinner.stop()
                logger.error(error_message)
                break
        if 'testDetails' in test['testExecutions'][0]:
            current_progress_message = test['testExecutions'][0]['testDetails']['progressMessages'][-1]
            if progress_message != current_progress_message:
                spinner.stop()
                logger.info(current_progress_message)
                spinner.start()
                progress_message = current_progress_message
        if test_state != current_state:
            spinner.stop()
            logger.info(current_state)
            spinner.start()
            test_state = current_state
        
        time.sleep(2)

    spinner.stop()
    
    # Download and parse test results
    logger.info('Downloading test results into {}..'.format(config['output']))
    runner.download('{}/{}-{}-en-portrait/test_result_1.xml'.format(config['results-bucket'], config['device']['model'], config['device']['version']), '{}/test_result_1.xml'.format(config['output']))
    logger.info('Run complete!')

if __name__ == "__main__":
   main()


