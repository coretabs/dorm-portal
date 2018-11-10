
let currentLang = localStorage.getItem("lang") || 'en'

const lang = require(`../locale/student.${currentLang}.json`);

export const language = lang[currentLang]