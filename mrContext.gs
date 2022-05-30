let DefDuration = 1 / 24 / 60 * 5;
let TimeConstruct = new Date()

class MrContext {
  constructor(spreadSheetURL, settings) { // class constructor
    this.timeConstruct = TimeConstruct;
    if (!spreadSheetURL) { throw new Error("spreadSheetURL"); }
    if (!`${spreadSheetURL}`.includes("https://docs.google.com/spreadsheets/")) { throw new Error("spreadSheetURL"); }
    Logger.log(`MrContext  constructor spreadSheetURL=${spreadSheetURL}`);
    this.spreadSheetURL = spreadSheetURL;
    this.spreadSheet = undefined;
    if (!settings) { throw new Error("settings"); }
    /** @type {MrSettings} */
    this.settings = settings;

    this.tMin = 20 * 1000;
  }


  getValueOr(sheetName, row, col, orValue = undefined) {
    let sheet = (() => { try { return this.getSheetByName(sheetName) } catch (err) { return undefined; } })();
    if (!sheet) { return orValue; }
    return sheet.getRange(row, col).getValue();
  }



  flush() {
    SpreadsheetApp.flush();
  }

  addLog(str) {
    if (this.addLog) {
      getContext().getSheetByName(getContext().sheetNameLogs).appendRow([undefined, new Date(), str]);
    }
  }


  getSpreadSheet() {
    // if (!this.spreadSheetURL) {
    //   this.spreadSheetApp = SpreadsheetApp.getActive();
    //   this.spreadSheetURL = this.spreadSheetApp.getUrl();
    // }

    if (!this.spreadSheet) {
      this.spreadSheet = SpreadsheetApp.openByUrl(this.spreadSheetURL);
    }
    return this.spreadSheet;
  }

  getSheetByName(sheetName, ssa = this.getSpreadSheet()) {
    // let ss = SpreadsheetApp.getActive();
    // let ssa = this.getSpreadsheetApp();

    let sh = ssa.getSheetByName(sheetName);
    if (!sh) { throw new Error(`нет листа с именем ${sheetName} в таблице ${ssa.getUrl()}  |  ${this.spreadSheetURL} `); }
    return sh;
  }

  addSheetByName(sheetName, templateSheetName) {
    // let ss = SpreadsheetApp.getActive();
    
    let templateSheet = this.getTemplateSheetByKey(templateSheetName);
    this.getSpreadSheet().insertSheet(sheetName, { template: templateSheet }).hideSheet();

  }


  getValueOr(sheetName, row, col, orValue = undefined) {
    let sheet = (() => { try { return this.getSheetByName(sheetName) } catch (err) { return undefined; } })();
    if (!sheet) { return orValue; }
    return sheet.getRange(row, col).getValue();
  }

  /** @param {SpreadsheetApp} ssa SpreadsheetApp    @returns {[string]} список листов в таблице */
  sheetNameArr(ssa = this.getSpreadSheet()) {
    let retArr = new Array();
    // let ss = SpreadsheetApp.getActive();
    // let ss = this.getSpreadsheetApp();
    let shs = ssa.getSheets();
    for (let i = 0; i < shs.length; i++) {
      retArr.push(shs[i].getSheetName());
    }
    return retArr;
  }

  getSettingsSheet() {
        // Logger.log(`MrContext  getSettingsSheet spreadSheetURL=${this.spreadSheetURL}`);
    if (!this.settingsSheet) {
      this.settingsSheet = new MrClassSettingsSheet(this.settings.sheetNames.Настройки, this);
    }
    return this.settingsSheet;
  }


  getTemplateSheetByKey(templateSheetName) {
    // Logger.log(`templateKey=${templateSheetName}`);

    // let settingsSheet = this.getSettingsSheet();
    // let urlШаблоныЛистов = settingsSheet.getValueByKey(this.settings.names.ШаблоныЛистов);
    // let context = new MrContext(urlШаблоныЛистов, this.settings);
    // // let ШаблоныЛистов = new MrClassSheetModel(this.settings.sheetNames.Настройки, context);
    // let sheetName = new MrContext(urlШаблоныЛистов, this.settings).getSettingsSheet().getValueByKey(templateSheetName);
    // if (!sheetName) { sheetName = this.settings.names.key_value; }
    let retSheet = this.getSheetByName(templateSheetName);
    // Logger.log(retSheet.getName());
    return retSheet;
  }




}





let mrContext = undefined;

/** @returns {MrContext} */
function getContext() {
  if (!mrContext) {
    mrContext = new MrContext(SpreadsheetApp.getActive().getUrl(), getSettings());
    // mrContext = new MrContext("sa");
  }
  return mrContext;
}

function fl_str(str) {
  if (!str) { return ""; }
  return str.toString().replace(/ +/g, ' ').trim().toUpperCase();
}

function mrErrToString(err) {
  let ret = "ОШИБКА ВЫПОЛНЕНИЯ СКРИПТА \n " + "\nдата время:" + new Date() + "\nname: " + err.name + "\nmessage: " + err.message + "\nstack: " + err.stack;
  Logger.log(ret);
  return ret;
}




function nr(A1) {
  A1 = A1.replace(/\d/g, '')
  let i, l, chr,
    sum = 0,
    A = "A".charCodeAt(0),
    radix = "Z".charCodeAt(0) - A + 1;
  for (i = 0, l = A1.length; i < l; i++) {
    chr = A1.charCodeAt(i);
    sum = sum * radix + chr - A + 1
  }
  return sum;
}


function nc(column) {
  column = parseInt("" + column);
  if (isNaN(column)) { throw ('файл mrColumnToNr функция nrCol(): не найдено буквенное обозначение для колонки "' + column + '"'); }

  column = column - 1;
  switch (column) {
    case 0: { return "A"; }
    case 1: { return "B"; }
    case 2: { return "C"; }
    case 3: { return "D"; }
    case 4: { return "E"; }
    case 5: { return "F"; }
    case 6: { return "G"; }
    case 7: { return "H"; }
    case 8: { return "I"; }
    case 9: { return "J"; }
    case 10: { return "K"; }
    case 11: { return "L"; }
    case 12: { return "M"; }
    case 13: { return "N"; }
    case 14: { return "O"; }
    case 15: { return "P"; }
    case 16: { return "Q"; }
    case 17: { return "R"; }
    case 18: { return "S"; }
    case 19: { return "T"; }
    case 20: { return "U"; }
    case 21: { return "V"; }
    case 22: { return "W"; }
    case 23: { return "X"; }
    case 24: { return "Y"; }
    case 25: { return "Z"; }

    default: {
      if (column > 25) { return `${nc(column / 26)}${nc((column % 26) + 1)}`; }
    }
  }

  throw new Error('файл mrColumnToNr функция nc(): не найдено буквенное обозначение для колонки "' + column + '"');

}
function responseToJSON(response) {
  let ret = new Object();

  ret["ResponseCode"] = response.getResponseCode();
  ret["Headers"] = response.getHeaders();
  ret["ContentText"] = response.getContentText();
  ret["Content"] = response.getContent();
  ret["Blob"] = response.getBlob();
  ret["AllHeaders"] = response.getAllHeaders();
  return JSON.stringify(ret);
}


function hasTime(duration, tMin = 20 * 1000) {
  let tDey = 24 * 60 * 60 * 1000;
  let tDuration = duration * tDey;
  // let tMin = 20 * 1000;
  let tStart = getContext().timeConstruct;
  let tNow = new Date();
  let tDef = tNow - tStart;
  let tHas = tDuration - tDef;

  // Logger.log(` 
  // duration=${duration}
  // tDuration=${tDuration}
  // tMim=${tMin}
  // tHas=${tHas}
  // `);

  if (tHas < tMin) { return false; }
  return true;
}


