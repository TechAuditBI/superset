import { FormatLocaleDefinition } from 'd3-format';


const NumberLocale: FormatLocaleDefinition = {
    decimal: ",",
    thousands: "\xa0",
    currency: ["$", ""],
    grouping: [3],
}

export default NumberLocale