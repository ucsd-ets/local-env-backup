from datetime import datetime as dt
import os, shutil, sys
import re

_kernel_name_description = "Kernel names can only contain ASCII letters and numbers and these separators:" \
    " - . _ (hyphen, period, and underscore)."


def fmt_now():
    return dt.now().strftime('%F_%H%M%S')


def backup_local(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(os.path.expanduser('~/.local'), dest)


def remove_local():
    src = os.path.expanduser('~/.local/lib')
    if os.path.exists(src):
        remove_dir(src)


def valid_label(label):
    return not re.search(r'[^a-zA-Z0-9._\-]', label)


def prompt_proceed_exit(display_str):
    prompt = input(display_str)
    if prompt.strip().lower() not in ['y', 'yes']:
        print('exit')
        sys.exit(0)

def prompt_proceed(display_str):
    prompt = input(display_str)
    return prompt.strip().lower() in ['y', 'yes']


def remove_dir(src):
    shutil.rmtree(src)
