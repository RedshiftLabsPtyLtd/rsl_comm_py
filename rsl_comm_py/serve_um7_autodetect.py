from shutil import copy
import os
import os.path
import stat


def serve_autodetect_script(target_dir='./'):
    """
    Copies UM7 autodetect script in target directory
    :param target_dir: directory to copy autodetect script to
    :return: 0 -- execution successful
    """
    autodetect_script = 'um7_autodetect.py'
    src_path = os.path.dirname(os.path.abspath(__file__))
    autodetect_script_abspath = os.path.join(src_path, autodetect_script)
    copy(autodetect_script_abspath, target_dir)
    # make copied file executable
    copied_file = os.path.join(target_dir, autodetect_script)
    st = os.stat(copied_file)
    os.chmod(copied_file, st.st_mode | stat.S_IEXEC)
