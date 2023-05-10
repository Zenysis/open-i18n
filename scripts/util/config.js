const prettier = require('prettier');

module.exports = {
  /** Options for babel parser */
  BABEL_OPTIONS: {
    plugins: ['jsx', 'flow', 'classProperties', 'decorators-legacy'],
    sourceType: 'module',
  },

  /** CSV column names for exporting/importing translations */
  COLUMN_TITLES: {
    ENGLISH: 'english',
    FILE: 'filename',
    ID: 'id',
    STATUS: 'status',
    TRANSLATION: 'translation',
  },

  /** Name given to any generated translation files */
  I18N_FILENAME: 'i18n.js',

  /** Translation file template location */
  I18N_TEMPLATE_FILEPATH: 'scripts/generator/i18n.template.txt',

  /**
   * Relative path from project root to JS codebase (js/jsx files that
   * import I18N). Will also be the location of the root i18n file.
   */
  I18N_ROOT: 'web/client',

  /** Full import root for files in the JS codebase */
  IMPORT_ROOT: `${process.cwd()}/${I18N_ROOT}`,

  /** Comment token to designate a translated value that may be outdated */
  OUT_OF_SYNC_TOKEN: ' @outOfSync',

  /** Options for prettier parser */
  PRETTIER_CONFIG: {
    ...prettier.resolveConfig.sync(null, {
      config: `${process.cwd()}/.prettierrc`,
    }),
    parser: 'flow',
  },
};
