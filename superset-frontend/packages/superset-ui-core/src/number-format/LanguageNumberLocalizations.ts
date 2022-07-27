import NumberLocales from './NumberLocales';

const LanguageNumberLocales = {
    ru: NumberLocales.NumberLocaleRU
}
// Global D3 formatting changes depending on the selected language
// If the language that is currently is use by user
// is not in LanguageNumberLocales we using default en locale.


export default LanguageNumberLocales