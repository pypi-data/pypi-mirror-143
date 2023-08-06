import logging
import logging.config
import os
import re
from signal import SIGTERM
from subprocess import DEVNULL, Popen
from time import sleep, time
from typing import Optional

import psutil

from .config import load_config_file, BadConfig, load_config_or_exit
from .lintmon import Lintmon
from .settings import (
    CONFIG_FILE,
    DEFAULT_IGNORED_DIRECTORY_NAMES,
    PID_FILE,
    STATE_DIR,
    STOP_FILE,
    STOP_WAIT_SECONDS,
)
from .utils import colour_text


LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'WARNING'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '%(levelname)s %(message)s'},
        'file': {'format': '%(asctime)s %(levelname)s: %(message)s'},
    },
    'handlers': {
        'console': {'level': LOG_LEVEL, 'class': 'logging.StreamHandler', 'formatter': 'simple'},
        'file': {
            'level': logging.INFO,
            'class': 'logging.FileHandler',
            'filename': '.lintmon/output.log',
            'formatter': 'file',
        },
        'null': {'class': 'logging.NullHandler'},
    },
    'root': {'level': 'DEBUG', 'handlers': ['console', 'file'], 'propagate': False},
}

try:
    logging.config.dictConfig(LOGGING)
except ValueError as exc:
    if "Unable to configure handler 'file'" not in str(exc):
        raise

log = logging.getLogger()


# --------------------------------------------------------------------------------------------------
# Entry points
# --------------------------------------------------------------------------------------------------
def lintmond():
    # if '--quiet' in sys.argv:
    #     root_logger = logging.getLogger()
    #     console_handler = first(h for h in root_logger.handlers if h.name == 'console')
    #     root_logger.removeHandler(console_handler)

    log.debug('lintmond main')

    lintmon = Lintmon(load_config_or_exit())
    lintmon.run()


def run_all():
    log.debug('Run all')
    config = load_config_or_exit()
    files = find_all_appropriate_files()
    lintmon = Lintmon(config)
    lintmon.update_sessions(files)

    print_sessions(lintmon.sessions)


def status():
    if not is_here():
        print('No lintmon.yaml in this directory')
        return

    if is_stopped():
        print('🛑 lintmon is stopped')
    else:
        if not lintmon_is_running():
            print('⚠️ lintmon is not running')
        else:
            print(f'✅ lintmon running pid {lintmon_pid()}')
    try:
        config = load_config_file(CONFIG_FILE)
    except BadConfig as exc:
        if 'No such config file' in str(exc):
            return 0
        print(colour_text(' ! ', background='red', foreground='white'), end='')
        print(' ' + str(exc))
        return 1

    config = load_config_or_exit()

    lintmon = Lintmon(config)
    lintmon.load_latest_sessions()

    print_sessions(lintmon.sessions)


def status_prompt():
    if not is_here():
        return

    os.makedirs(STATE_DIR, exist_ok=True)

    if is_stopped():
        print(colour_text(' S ', background='red', foreground='white'), end='')
        return

    ensure_lintmon_is_running()

    try:
        config = load_config_file(CONFIG_FILE)
    except BadConfig as exc:
        if 'No such config file' in str(exc):
            return 0
        print(colour_text(' ! ', background='red', foreground='white'), end='')
        return 1

    config = load_config_or_exit()

    lintmon = Lintmon(config)
    lintmon.load_latest_sessions()

    print(lintmon.badges, end='')
    log.debug('status_prompt finished')


def start():
    if is_stopped():
        os.remove(STOP_FILE)

    ensure_lintmon_is_running()


def stop():
    if not is_stopped():
        with open(STOP_FILE, 'w'):
            pass

    pid = lintmon_pid()
    if pid is None:
        print('Not running')
        return

    print(f'Sending SIGTERM to {pid}')
    os.kill(pid, SIGTERM)

    print(f'Waiting up to {STOP_WAIT_SECONDS} for termination...')
    start = time()
    while time() < start + STOP_WAIT_SECONDS:
        if not lintmon_is_running():
            print('Terminated')
            return

        sleep(0.1)

    print(f'{pid} did not terminate')


# --------------------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------------------
def find_all_appropriate_files():
    full_file_paths = []
    for dirpath, subdirs, files in os.walk(os.curdir):
        for file in files:
            full_file_paths.append(os.path.join(dirpath, file))

        for ignored_subdir in DEFAULT_IGNORED_DIRECTORY_NAMES:
            try:
                subdirs.remove(ignored_subdir)
            except ValueError:
                pass

    return full_file_paths


def is_here():
    return os.path.exists(CONFIG_FILE)


def is_stopped():
    return os.path.exists(STOP_FILE)


def lintmon_pid() -> Optional[int]:
    if not os.path.exists(PID_FILE):
        log.debug('no pid file %s', PID_FILE)
        return None

    with open(PID_FILE) as pf:
        pid_line = pf.readline()

    mo = re.match(r'(\d+)', pid_line)
    if not mo:
        log.debug('Pid file does not match regex %s', pid_line)
        return None

    pid = int(mo.group(1))
    pid_alive = psutil.pid_exists(pid)

    if not pid_alive:
        log.debug('Pid %s is not alive', pid)
        os.remove(PID_FILE)
        return None
    return pid


def lintmon_is_running():
    return lintmon_pid() is not None


def print_sessions(sessions):
    for ms in sessions:
        if len(ms.problem_lines) == 0:
            print(f'✅ {ms} clean')
            continue

        coloured = ms.badge
        print(f'{coloured} {ms} output:')
        for ol in (pl for pls in ms.problem_lines.values() for pl in pls):
            print(f'  {ol}')


def run_lintmond():
    print('Starting lintmond...')
    proc = Popen(['lintmond', '--quiet'], stdin=DEVNULL, stderr=DEVNULL, stdout=DEVNULL)
    log.debug('lintmond running %s', proc.pid)

    with open(PID_FILE, 'w') as pf:
        pf.write(str(proc.pid))


def ensure_lintmon_is_running():
    if lintmon_is_running():
        log.info('lintmon running')
        return

    run_lintmond()
