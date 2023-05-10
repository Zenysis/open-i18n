import os
import subprocess
from typing import List, Optional

# Relative path from project root to JS codebase (js/jsx files that import I18N)
I18N_ROOT = 'web/client'


def find_src_root() -> str:
    '''Return the project source root directory.'''
    dir = os.getcwd()
    while (
        dir
        and dir != '/'
        and os.path.isdir(dir)
        and not os.path.exists(os.path.join(dir, '.git'))
    ):
        dir = os.path.dirname(dir)
    return dir


def get_absolute_filepath(filename: str) -> Optional[str]:
    """Return the absolute path for the filename, if it exists."""
    if not filename:
        return None

    if os.path.exists(filename):
        return os.path.normpath(os.path.abspath(filename))

    if filename[0] == '/':
        filename = filename[1:]
    abs_path = os.path.normpath(os.path.join(find_src_root(), filename))
    if os.path.exists(abs_path):
        return abs_path

    return None


def get_translation_files(exclude_root: bool = False) -> List[str]:
    '''Get a list of all files in project with the filename `i18n.js`.

    Args:
        exclude_root: if true, exclude top-level `i18n.js` file.

    Returns:
        List[str]
    '''
    root_dir = f'{find_src_root()}/{I18N_ROOT}'
    find_args = ['find', root_dir, '-name', 'i18n.js']

    if exclude_root:
        find_args += ['-not', '-path', f'{root_dir}/i18n.js']

    results: str = (
        subprocess.Popen(find_args, stdout=subprocess.PIPE)
        .communicate()[0]
        .decode('utf-8')
    )
    return results.splitlines()
