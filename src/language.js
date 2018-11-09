
let currentLang = 'en'

const lang = require(`../locale/student.${currentLang}.json`);

export const language = lang[currentLang]

// export const language = {
//   "dormSearch": {
//     "heading":"Find Dormitories in EMU"
//   }
// }