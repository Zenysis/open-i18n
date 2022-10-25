const MULTISPACE_REGEX = /\s\s+/g;
const NEWLINE_REGEX = /(\r\n|\n|\r)/g;
const PERIOD_REGEX = /\./g;

/**
 * In case the id has multiple spaces or new lines or periods, we clean them up
 * here for consistency. Replace periods because dot-separation breaks
 * counterpart ids.
 */
function cleanTranslationId(id) {
  return id
    .replace(NEWLINE_REGEX, " ")
    .trim()
    .replace(MULTISPACE_REGEX, " ")
    .replace(PERIOD_REGEX, "_");
}

module.exports = {
  MULTISPACE_REGEX,
  NEWLINE_REGEX,
  PERIOD_REGEX,
  cleanTranslationId,
};
