import os
import stat

from pathlib import Path
from shutil import copy


def serve_autodetect_script(target_dir='./'):
    """
    Copies RSL autodetect script in target directory
    :param target_dir: directory to copy autodetect script to
    :return: 0 -- execution successful
    """
    autodetect_script = 'rsl_autodetect.py'
    src_path = Path(__file__).parent
    target_dir = Path(target_dir)
    autodetect_script_abspath = src_path / autodetect_script
    copy(autodetect_script_abspath, target_dir)
    # make copied file executable
    copied_file = target_dir / autodetect_script
    st = os.stat(copied_file)
    os.chmod(copied_file, st.st_mode | stat.S_IEXEC)
