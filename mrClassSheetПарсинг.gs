class MrClassSheetПарсинг extends MrClassSheetModel {
  constructor(sheetName, context) {
    super(sheetName, context);

    this.ranges = {
      urlForNewCenal: "N1",
      Помощник: {
        обработан: "C2",
      },
      Обход: {
        обработан: "D2",
      },

      Отправлен: {
        отправлен: "E2",

      },

    };
  }

  /** @param {[]} keys */
  add_new_keys(keys) {
    if (!Array.isArray(keys)) { return; }
    keys = keys.map((v, i, arr) => { return [v]; });
    this.sheet.getRange(this.row.body.last + 1, this.col.key, keys.length, 1).setValues(keys);
  }

  getNextRowAfter(row) {
    return row + 1;
  }

  getNextObjForParse() {
    /** @type {Obj} */
    let retObj = undefined;
    let lock = LockService.getScriptLock();
    try {
      lock.waitLock(1000 * 60 * 29); // подождите 60 * 29 секунд, пока другие не воспользуются разделом кода, и заблокируйте его, чтобы остановить, а затем продолжите

      while (!retObj) {
        let row = this.sheet.getRange(this.ranges.Отправлен.отправлен).getValue();
        if (!row) { row = this.row.body.first - 1; }
        row = this.getNextRowAfter(row);

        if (row <= this.row.body.last) {

          let vls = this.sheet.getRange(row, 1, 1, this.col.last).getValues();
          vls = vls.map((v, i, arr) => { return [row + i].concat(v); });
          retObj = this.toObj(vls[0]);


        } else {
          retObj = undefined;
          break;
        }

        // Logger.log(retObj);

        let skip = false;

        if (!retObj.key) {
          skip = true;
          // Logger.log("key");
        }
        if (retObj.value) {
          // skip = true;
          // Logger.log("value");
        }
        if (retObj.isValid === false) {
          skip = true;
          // Logger.log("isValid");
        }
        if (retObj.on === false) {
          skip = true;
          // Logger.log("on");
        }

        if (skip) {
          retObj = undefined;
          // Logger.log("skip");
        }

        this.sheet.getRange(this.ranges.Отправлен.отправлен).setValue(row);
         if (retObj) { this.setValue(retObj.row, this.col.on, true); }
         SpreadsheetApp.flush();  
      }

    } catch (err) {
      mrErrToString(err);
      let str = "Наверное очередь занята";
      Logger.log(str);

    } finally {
      lock.releaseLock();
    }

   
    return retObj;
  }

  /** @param {Obj} obj */
  saveObjAfterParse(obj) {

    obj.value = JSON.stringify(obj.prices);
    obj.on = false;
    // obj.error = "sasa";
    obj.isValid = (!obj.error ? true : false);
    obj.isValid = (!obj.value ? false : true);
    // obj.isValid = (!obj.prices ? false : true);
    obj.last = new Date();
    // obj.value = JSON.stringify(obj);
    this.saveObj(obj);

  }


}


function testNestMrClassSheetПарсинг() {
  let mrClassSheetПарсинг = new MrClassSheetПарсинг(getSettings().sheetNames.Парсинг, getContext());
  let objNext = mrClassSheetПарсинг.getNextObjForParse();
  Logger.log(objNext);
  objNext.prices = [1, 2, 3, 4, 5];
  SpreadsheetApp.flush()
  // Utilities.sleep(10000);
  mrClassSheetПарсинг.saveObjAfterParse(objNext);
  Logger.log(JSON.stringify(objNext));
}








