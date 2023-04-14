import subprocess

from scripts.translations_util import find_src_root


def translations_import(args) -> None:
    '''This command imports all translations in `filename` and adds the
    translated values to the appropriate i18n.js files.
    1. Open the file at `filename` and validate that there is at least
       an id column and a translation column.
    2. Read in all (id, translated value) pairs.
    3. For each translation, use the id to determine which i18n.js file to add
       the translation to.
    4. Write (id, translated value) to the appropriate i18n.js files.
    '''
    subprocess.run(
        f'node scripts/importer/main.js {args.locale} {args.input_file}',
        cwd=find_src_root(),
        shell=True,
        check=True,
    )
