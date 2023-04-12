# open-i18n

TODO — publishing library

- [ ] Replace use of internal python libraries in scripts
- [ ] Generalize references to `web/client` and remove root directory dependencies

- [ ] Setup/install instructions
- [ ] Demo usage

---

# React API docs

There are two options for introducing translated text to client-side code: a `I18N.text()` function call or the `<I18N>` JSX element.

## I18N.text()

The function signature differs for single and pluralized text translations. Note that for both, the config does not support interpolating React Nodes, because this function returns a string. If you need to support interpolating React Nodes, then you should use the <I18N> component.

### Singular string translations

```
I18N.text(contents, id?, config?)
```

Arguments:

- `contents`: String that should be translated.
- `id?`: Optional string ID to assign translation.
- `config?`: Optional config object for string interpolation.

```
// Examples
const str = I18N.text('This is my text');
const str = I18N.text('Translate this text', 'text-id');
// With interpolation
// The sprintf-derived pattern is '%(variable)s'. The 's' is not printed.
const str = I18N.text('Hello %(name)s', { name: 'Pablo' });
const str = I18N.text('Hello %(name)s', 'my-id', { name: 'Pablo' });
```

### Pluralized string translations

```
I18N.text(contents, id, config)
```

Arguments:

- `contents`: Object with zero, one, and other keys, with associated values to display based on count.
- `id`: Required string ID.
- `config`: Config object for determining translation plurality (and optionally, string interpolation). The count key is required and must store a numeric value.

```
// Examples
const countVar = 1;
const str = I18N.text(
  {
    zero: 'Text for count=0',
    one: 'Text for count=1',
    other: 'Text for -1>=count>1'
  },
  'plural-id',
  { count: countVar },
});

// With interpolation
const str = I18N.text(
  { zero: 'No %(item)s', one: 'One %(item)s', other: 'Multiple %(item)s' },
  'plural-str-id',
  { count: 0, item: "fish" },
);
```

### Translations by reference

Existing I18N translations may be used in multiple places, by reference.

```
const str = I18N.textById('This is my text');
const str = I18N.textById('my-id', { name: 'Pablo' });
const str = I18N.textById('plural-id', { count: 1 });
```

## JSX: `<I18N>`

Basic usage

```
<I18N>Hello, this is translatable text.</I18N>
<I18N id="my-id">Here is more translatable text.</I18N>
```

### String interpolation

```
<I18N name={someVar}>
  Welcome, %(name)s
</I18N>

<I18N id="greeting" name={someVar}>
  Welcome, %(name)s
</I18N>
```

### Translations by reference

```
<I18N.Ref id="Hello, this is translatable text"/>
<I18N.Ref id="my-id"/>
// With interpolation
<I18N.Ref id="greeting" name="Pablo" />
```

### React component injection

It's common to want to add markup or React components to translations, such as when trying to add styling (e.g. bold) to part of a translation. This is supported by injecting React components using interpolation:

```
<I18N name={<b>{someVar}</b>}>
Hello %(name)s, how are you?
</I18N>

<I18N someDropdown={<Dropdown>{options}</Dropdown>}>
I want to choose %(someDropdown)s option
</I18N>
```

### Pluralization

Currently, `<I18N>` does not support pluralized translations. Instead, use the `I18N.text()` function inside JSX, e.g. `<Button>{I18N.text(…)}</Button>`.

## Note: reserved keywords

`%` is a reserved character and should be used a double character `%%` like `I18N.text('%% of users')` to give "% of users". This is also true for translations in other languages. If the page does not load with the error `Uncaught SyntaxError: [sprintf] unexpected placeholder` in the console, then this is the issue.

The following keys are reserved and will not work as interpolation variables: "children", "id", "locale", and "fallback".

"count" is a reserved keyword only for singular strings, but for pluralized strings, it may be used for interpolation (i.e. the "count" key is required for pluralization, and you may use "%(count)s" to print its value). Remember that it can only hold a numeric value as required by the pluralization API.

# Scripting

## Keeping translations synchronized

The `generate_translations` script handles the following cases:

- New I18N text added → translation added in English\*
- I18N text deleted → translation deleted from all languages
- I18N text ID changed → translation ID updated in all languages
- I18N text value changed → English translation value updated; all other translations tagged as @outOfSync since the non-English text may be incorrect\*\*

\*New I18N text keys/values are initially only added in English. When non-English languages are missing a translation key, the platform will default to the English text.

\*\*To find all @outOfSync tags, run `yarn cli-translations list_out_of_sync`.

## How are non-English translations added/updated?

1. **Export**

   _Export the translations using `yarn cli-translations export --locale <locale to translate> --out <out filepath>`._

- CSV columns are filepath, id, english, translation, status where status is "Up to date," "Missing," or "Out of sync."
- Export translations of a certain status by adding `--missing` and/or `--out_of_sync` flag.
- Pluralized translation values are exported as three different rows (all with the same key).

2. **Update**

   _Your translator will add translated values to the "translation" column in the exported CSV._

3. **Import**

   _Given a CSV file with, at least, the three required columns ("id", "filename", and "translation"), run `yarn cli-translations import --locale <locale code> --input <csv filepath>`_

## Adding a new locale

To add a new locale, simply run `yarn cli-translations add_locale --locale <code>` with the ISO code of your new locale. This will create empty {} objects for the new locale in every existing i18n.js file and additionally add the code to the list of acceptable locales so that the import script will work.

# Contribution Suggestions

- [ ] Expand reference capabilities (i.e. `<I18N.Ref>` and `I18N.textById()`) to accept identifiers, not just string literals, as translations ids. See NOTEs in `scripts/translations/collectReferencesFromFile.js` and remember that `getPropStringFromI18NJSX` will need to return non-string props.
- [ ] Refactor `_checkForReferenceMatch` in `scripts/translations/listDanglingReferences.js` to build a set of all ids for faster lookup.
- [ ] Refactor `_findFilesThatImportI18N` in `scripts/translations/generateTranslations.js` to use ripgrep `rg` for performance e.g. `rg -l -t js '^import I18N' '${process.cwd()}/web/client'`
- [ ] Adjust locale codes to comply with ICU standard: https://www.localeplanet.com/icu/
