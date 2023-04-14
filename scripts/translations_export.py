import subprocess

from scripts.translations_util import get_translation_files, find_src_root


def translations_export(args) -> None:
    '''This command exports all translations of a given `locale` to
    a specified output CSV.
    1. Find all i18n.js files
    2. Collect all 'en' translations
    3. Collect all translations for the given `locale`
    4. Add all translations to a CSV
    '''
    print('Scanning files...')
    filenames = get_translation_files()

    num_files = len(filenames)
    pluralized_file = 'file' if num_files == 1 else 'files'
    print(f'Found {num_files} i18n.js {pluralized_file}')

    args = [
        '--missing' if args.missing else '',
        '--out_of_sync' if args.out_of_sync else '',
        args.locale,
        args.out,
        *(f"'{f}'" for f in filenames),
    ]
    args_str = ' '.join(args)

    subprocess.run(
        f'node scripts/exporter/main.js {args_str}',
        cwd=find_src_root(),
        shell=True,
        check=True,
    )
