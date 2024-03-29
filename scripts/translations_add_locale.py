import subprocess
from argparse import Namespace

from scripts.translations_util import get_translation_files, find_src_root


def translations_add_locale(args: Namespace) -> None:
    '''This adds the new locale to the project's i18n library. It will:
    1. Find all directory-level i18n.js files.
    2. Insert an empty translation object for the new locale
    into the `translations` dictionary in each file.
    '''
    print('Scanning files...')
    filenames = get_translation_files(True)

    num_files = len(filenames)
    pluralized_file = 'file' if num_files == 1 else 'files'
    print(f'Found {num_files} directory-level i18n.js {pluralized_file}')

    files_arg = "'%s'" % ("' '".join(filenames))

    subprocess.run(
        f'node scripts/localeAdder/main.js {args.locale} {files_arg}',
        cwd=find_src_root(),
        shell=True,
        check=True,
    )
