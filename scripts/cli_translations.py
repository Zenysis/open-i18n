#!/usr/bin/env python
import argparse
import sys

from scripts.translations_export import translations_export
from scripts.translations_generate import translations_generate

from scripts.translations_watch import translations_watch
from scripts.translations_list_dangling import translations_list_dangling
from scripts.translations_list_dangling_ref import (
    translations_list_dangling_ref,
)
from scripts.translations_list_out_of_sync import (
    translations_list_out_of_sync,
)
from scripts.translations_import import translations_import
from scripts.translations_add_locale import translations_add_locale


def main():
    """A CLI to execute common translation operations."""
    parser = argparse.ArgumentParser(
        description="CLI to execute common translation operations."
    )
    subparsers = parser.add_subparsers(dest="subcommand")

    # generate subcommand
    generate_parser = subparsers.add_parser(
        "generate", help="Generate new translation files and keys for entire codebase."
    )
    generate_parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Use this flag to print out more detailed information",
    )
    generate_parser.set_defaults(func=translations_generate)

    # list_dangling_translations subcommand
    dangling_translations_parser = subparsers.add_parser(
        "list_dangling_translations", help="List the IDs of all dangling translations."
    )
    dangling_translations_parser.add_argument(
        "--base_locale",
        default="en",
        type=str,
        required=False,
        help='Base locale used to define dangling translations (default \"en\")',
    )
    dangling_translations_parser.set_defaults(func=translations_list_dangling)

    # list_dangling_references subcommand
    dangling_references_parser = subparsers.add_parser(
        "list_dangling_references",
        help="List the IDs of all translation references that do not match a translation.",
    )
    dangling_references_parser.set_defaults(func=translations_list_dangling_ref)

    # watch subcommand
    watch_parser = subparsers.add_parser(
        "watch",
        help="Watch for new translations and automatically update i18n.js files.",
    )
    watch_parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Use this flag to print out more detailed information",
    )
    watch_parser.set_defaults(func=translations_watch)

    # export subcommand
    export_parser = subparsers.add_parser(
        "export",
        help="Export all I18N translations to a CSV.",
    )
    export_parser.add_argument(
        "--out",
        type=str,
        required=True,
        help="Filename in which to store output",
    )
    export_parser.add_argument(
        "--locale",
        type=str,
        required=True,
        help="Locale to target for export (must run one at a time)",
    )
    export_parser.add_argument(
        "--missing",
        action="store_true",
        required=False,
        help="When set, only missing translations will be exported",
    )
    export_parser.add_argument(
        "--out_of_sync",
        action="store_true",
        required=False,
        help="When set, only out-of-sync translations will be exported",
    )
    export_parser.set_defaults(func=translations_export)

    # list_out_of_sync subcommand
    out_of_sync_parser = subparsers.add_parser(
        "list_out_of_sync",
        help="List all translations in i18n.js files tagged as out of sync.",
    )
    out_of_sync_parser.set_defaults(func=translations_list_out_of_sync)

    # import subcommand
    import_parser = subparsers.add_parser(
        "import",
        help="Import translations CSV into app. Required columns: filename, id, translation.",
    )
    import_parser.add_argument(
        "--locale",
        type=str,
        required=True,
        help="Locale into which to import new translations",
    )
    import_parser.add_argument(
        "--input_file",
        type=str,
        required=True,
        help="Filename with translated text to upload to app",
    )
    import_parser.set_defaults(func=translations_import)

    # add_locale subcommand
    add_locale_parser = subparsers.add_parser(
        "add_locale",
        help="Add a new locale to the project.",
    )
    add_locale_parser.add_argument(
        "--locale",
        type=str,
        required=True,
        help="IDO code for new locale",
    )
    add_locale_parser.set_defaults(func=translations_add_locale)

    args = parser.parse_args()
    if args.subcommand is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    sys.exit(main())
