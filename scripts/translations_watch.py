import subprocess
from argparse import Namespace

from scripts.translations_generate import translations_generate
from scripts.translations_util import (
    find_src_root,
    get_absolute_filepath,
    I18N_ROOT,
)

TRANSLATIONS_MAIN = get_absolute_filepath('scripts/watcher/main.js')
SRC_ROOT = find_src_root()


def translations_watch(args: Namespace) -> None:
    '''This command starts a watchman server that will send a filepath to the
    watcher script every time a file changes. The watcher script will handle
    generating translations for the modified file.
    '''
    print('Starting translations watch server...')
    verbose_arg = '--verbose' if args.verbose else ''

    # first, generate all translations to make sure we are up-to-date
    translations_generate(args)

    # now start up the watchman server to detect any new changes
    subprocess.run(
        f"watchman-wait {SRC_ROOT} -p '{I18N_ROOT}/**/*.js' '{I18N_ROOT}/**/*.jsx' "
        f'--max-events 0 | node {TRANSLATIONS_MAIN} {SRC_ROOT} {verbose_arg}',
        cwd=SRC_ROOT,
        shell=True,
        check=True,
    )
