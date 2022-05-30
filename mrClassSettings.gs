
function fl_str(str) {
  if (!str) { return ""; }
  return str.toString().replace(/ +/g, ' ').trim().toUpperCase();
}

class MrSettings {
  constructor() {
    this.sheetNames = {
      Аналитика: "Аналитика",
      Парсинг:"Парсинг",
      Настройки: "Настройки",
    }

    // this.sheetTemplate = {
    //   YouTybeКанал: "ШаблоныЛистаYouTybeКанал",
    //   YouTybeКаналы: "YouTybeКаналы",
    //   Настройки: "Настройки",
    //   Пустой:"Пустой",
    // }

    // this.names = {
    //   ШаблоныЛистов: "ШаблоныЛистов",
    //   UrlForNewCenal: "UrlForNewCenal",
    //   key_value:"key_value",
    // }
    // this.settings = this;
  }


  /** @param {object} newSettings */
  setSettings(newSettings) {
    if (typeof newSettings != "object") { return; }
    for (let key in newSettings) {
      this[key] = newSettings[key];
    }
  }

}

let mrSettings = undefined;

/** @returns {MrSettings} */
function getSettings() {
  if (!mrSettings) {
    mrSettings = new MrSettings();
  }
  return mrSettings;
}

function setSettings(newSettings) {
  getSettings().setSettings(newSettings);
}



class MrClassSettingsSheet extends MrClassSheetModel {
  constructor(sheetName, context) {
      super(sheetName, context);
  }
}



