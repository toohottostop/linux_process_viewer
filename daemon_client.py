import pathlib
import subprocess
import shlex
import requests
import json
import time
import logging
import daemon


def set_logger(log_file_path):
    logger = logging.getLogger('monitor_ps')
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)

    formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(formatstr, "%Y-%m-%d %H:%M:%S")

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return file_handler, logger


def parse_and_send_data():
    headers = ['pid', 'cpu_usage', 'memory_usage', 'command']
    command_1 = 'ps -eo pid,pcpu,pmem,comm --sort -pcpu'
    command_2 = 'head -5'
    logger.debug('In function "parse_and_send_data". Enter in loop')
    while True:
        process_1 = subprocess.Popen(shlex.split(command_1),
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
        process_2 = subprocess.Popen(shlex.split(command_2),
                                     stdin=process_1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     encoding='utf8')
        process_1.stdout.close()
        stdout, stderr = process_2.communicate()
        if stderr:
            logger.error('Error occurred: stderr')
        else:
            logger.debug('Get stdout and forming json...')

        raw_data = []
        for line in stdout.split('\n'):
            if line and 'PID' not in line:
                raw_data.append(line.split())
        data = [dict(zip(headers, row)) for row in raw_data]

        try:
            response = requests.post(
                'http://127.0.0.1:8000/monitor',
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'}
            )
            logger.debug('Send request')
        except requests.exceptions.ConnectionError:
            logger.error('Connection problems')
        time.sleep(10)


def start_daemon(file_handler):
    logger.debug('Start daemon')
    with daemon.DaemonContext(
            working_directory=pathlib.Path(__file__).parent,
            umask=0o002,
            files_preserve=[file_handler.stream]):
        parse_and_send_data()


if __name__ == "__main__":
    file_handler, logger = set_logger('logs/daemon_client_log.log')
    start_daemon(file_handler)
