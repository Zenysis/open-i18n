import subprocess

from scripts.translations_util import get_translation_files, find_src_root


def translations_list_out_of_sync(_args) -> None:
    '''This finds all i18n.js files that contains @outOfSync tags and prints
    the tagged translations.
    1. Find all i18n.js files
    2. Inspect each file for @outOfSync comments
    3. For all files in which comment was found, print tagged translations
    '''
    print('Scanning files...')
    filenames = get_translation_files(True)

    num_files = len(filenames)
    pluralized_file = 'file' if num_files == 1 else 'files'
    print(f'Found {num_files} i18n.js {pluralized_file}')

    files_arg = "'%s'" % ("' '".join(filenames))

    subprocess.run(
        f'node scripts/synchronizer/outOfSyncMain.js {files_arg}',
        cwd=find_src_root(),
        shell=True,
        check=True,
    )
