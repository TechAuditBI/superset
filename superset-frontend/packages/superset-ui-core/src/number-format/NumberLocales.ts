import { FormatLocaleDefinition } from 'd3-format';


const NumberLocaleRU: FormatLocaleDefinition = {
    decimal: ",",
    thousands: "\xa0",
    currency: ["", "₽"],
    grouping: [3],
}

const NumberLocaleDOLLAR: FormatLocaleDefinition = {
    decimal: ".",
    thousands: ",",
    currency: ["$", ""],
    grouping: [3],
}

const NumberLocales = {
    NumberLocaleRU,
    NumberLocaleDOLLAR
}
export default NumberLocales