/** @typedef {Object} Obj
 * @property {number} row
 * @property {string} key
 * @property {boolean} on
 * @property {string} last
 * @property {boolean} isValid	
 * @property {string} value
 */


function getMrClassSheetModel() {
  return MrClassSheetModel;
}

class MrClassSheetModel {

  constructor(sheetName, context) {
    if (!context) { throw new Error("context"); }
    this.sheetName = sheetName;
    /** @type {MrContext} */
    this.context = context;
    this.sheet = this.context.getSheetByName(this.sheetName);
    this.init();

  }

  log() {
    this.getMap();
    Logger.log(``);
    Logger.log(`vvvvvvvvvvvvvvv${this.sheetName}vvvvvvvvvvvvvvv`);
    Logger.log(`${this.sheetName} | ${JSON.stringify(this)}`);
    Logger.log(`this.head_key=${JSON.stringify(this.head_key)}`);
    Logger.log(`this.col     =${JSON.stringify(this.col)}`);
    // Logger.log(`this.vls     =${JSON.stringify(this.vls)}`);
    Logger.log(`this.map.size=${JSON.stringify(this.map.size)}`);
    Logger.log(`this.getKeys=${JSON.stringify(this.getKeys())}`);
    for (let [key, value] of this.getMap()) {
      Logger.log(`${key} | ${JSON.stringify(value)} `);

    }

    // for (let [key, value] of this.getMap()) {
    //   Logger.log(`${key} | ${JSON.stringify(this.toObj(value))} `);
    // }

    // for (let [key, value] of this.getMap()) {
    //   Logger.log(`${key} | ${this.toArr((this.toObj(value)))} `);
    // }


    Logger.log(`^^^^^^^^^^^^^^^${this.sheetName}^^^^^^^^^^^^^^^`);
    Logger.log(``);

  }

  init() {
    this.row = {
      head: {
        first: 1,
        changed: 8,
        last: 10,
        key: 10,
      },

      body: {
        first: 11,
        last: 11,
      }
    }

    this.col = {
      row: undefined,
      on: undefined,
      isValid: undefined,
      key: undefined,
      value: undefined,
      last: this.sheet.getLastColumn(),
    }
    // this.head_key = ["row"];   

    this.row.body.last = this.sheet.getLastRow();
    if (this.row.body.last < this.row.body.first) { this.row.body.last = this.row.body.first; }
    if (this.col.last == 0) { this.col.last = 1; }
    this.head_key = [].concat("row", this.sheet.getRange(this.row.head.key, 1, 1, this.col.last).getValues()[0]);
    this.changed_key = [].concat(false, this.sheet.getRange(this.row.head.changed, 1, 1, this.col.last).getValues()[0]);

    for (let i = this.head_key.length - 1; i >= 0; i--) {
      let key = this.head_key[i];
      if (!key) { continue; }
      this.col[key] = i;
    }
    if (!this.col.key) { this.col.key = this.col.row; }

  }

  reset() {
    this.row.body.last = this.sheet.getLastRow();
    this.vls = undefined;
    this.map = undefined;
  }

  getValues() {
    if (!this.vls) {
      let vls = this.sheet.getRange(this.row.body.first, 1, this.row.body.last - this.row.body.first + 1, this.col.last).getValues();
      vls = vls.map((v, i, arr) => { return [this.row.body.first + i].concat(v); });
      this.vls = vls;
    }
    return this.vls;
  }



  getMap() {
    if (!this.map) {
      this.map = new Map();
      let vls = this.sheet.getRange(this.row.body.first, 1, this.row.body.last - this.row.body.first + 1, this.col.last).getValues();
      vls.forEach((v, i, arr) => {
        v = [this.row.body.first + i].concat(v)
        let key = v[this.col.key];
        if (`${key}` == "") { return; }
        this.map.set(key, this.toObj(v));
      });
    }
    return this.map;
  }

  getKeys() {
    return [...this.getMap().keys()];
  }

  getRowByKey(key) {
    /** @type {Obj} */
    let obj = this.getObj(key);
    if (!obj) { return; }
    let row = obj.row;
    if (!row) { return; }
    if (row < this.row.body.first) { return; }
    return row;
  }

  /** @returns {Obj} */
  getObj(key) {
    return this.getMap().get(key);
  }

  getValueByKey(key, value_key = "value") {
    if (!this.head_key.includes(value_key)) { return; }
    let obj = this.getObj(key);
    if (!obj) { return; }
    return obj[value_key];
  }

  /** @param {Obj} obj*/
  saveObj(obj) {
    if (Array.isArray(obj)) {
      throw new Error(`is not object ${obj}`);
    }

    if (typeof obj != "object") {
      throw new Error(`is not object ${obj}`);

    }


    let row = 0;
    if (!row) { row = obj.row; }
    if (!row) { row = this.getRowByKey(obj.key); }
    if (!row) { row = 0; }
    if (typeof row != "number") { row = 0; };

    obj = this.toArr(obj);
    obj.splice(0, 1);
    if (row <= 0) {
      this.sheet.appendRow(obj);

    } else {
      this.sheet.getRange(row, 1, 1, obj.length).setValues([obj]);
    }



    this.reset();
  }

  appendObj(obj) {

    obj.row = undefined;
    this.saveObj(obj);

  }

  delObj(key) {
    let row = this.getRowByKey(key);
    if (!row) { return; }
    if (row < this.row.body.first) { return; }
    this.sheet.getRange(row, 1, 1, this.col.last).clearContent();
    // this.sheet.deleteRow(row);
    this.getMap().delete(key);
    this.reset();
  }

  offByKey(key) {
    let row = this.getRowByKey(key);
    this.setValue(row, this.col.on, false);
    this.getObj(key).on = false;
    // this.reset();
  }

  onByKey(key) {
    let row = this.getRowByKey(key);
    this.setValue(row, this.col.on, true);
    this.getObj(key).on = true;
    // this.reset();
  }


  setValue(row, col, value) {
    if (!row) { return; }
    if (row < this.row.body.first) { return; }
    if (!col) { return; }
    this.sheet.getRange(row, col).setValue(value);
  }

  /** @param {Obj} obj , @returns {[]} */
  toArr(obj) {

    let retArr = new Array(this.head_key.length);
    for (let i = this.head_key.length - 1; i >= 0; i--) {
      let key = this.head_key[i];
      // Logger.log(`i=${i}  key=${key} = val=${obj[key]}`);
      if (!key) { continue; }
      retArr[i] = obj[key];
    }
    return retArr;
  }

  toObj(arr) {
    let retObj = new Object();
    // Logger.log()
    for (let i = this.head_key.length - 1; i >= 0; i--) {
      let key = this.head_key[i];
      if (!key) { continue; }
      retObj[key] = arr[i];
    }
    return retObj;
  }

  optimize() {
    // return
    SpreadsheetApp.flush();
    this.reset();
    this.map = undefined;
    let map = this.getMap();
    let vls = [...map.values()].map((obj, i, arr) => { let ret = this.toArr(obj); ret.splice(0, 1); return ret; });

    this.sheet.getRange(this.row.body.first, 1, this.row.body.last - this.row.body.first + 1, this.col.last).clearContent();
    if (vls.length == 0) { return; }
    this.sheet.getRange(this.row.body.first, 1, vls.length, vls[0].length).setValues(vls);
    this.reset();
  }

  /** @param {Obj} obj */
  isChanged(obj) {
    let snapshotObj = this.makeSnapshot(obj);
    if (JSON.stringify(snapshotObj) === obj.last) { return false; }
    return true;
  }

  /** @param {Obj} obj */
  makeSnapshot(obj) {
    let retObj = new Object();
    for (let i = this.head_key.length - 1; i >= 0; i--) {
      if (this.changed_key[i] !== true) { continue; }
      let key = this.head_key[i];
      if (!key) { continue; }
      retObj[key] = obj[key];
    }
    return retObj;
  }

}




// class MrClassSheetModelExtends extends MrClassSheetModel {
//   constructor(sheetName, context) {
//     let aaas = 13;
//     // this.col["ЖЖ"]=100; 
//     super(sheetName, context);

//   }

// }
