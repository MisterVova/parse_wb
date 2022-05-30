// https://script.google.com/macros/s/AKfycbx2Jm6G5vZLIgOYE8Bd2FWRevyn6KQKAGgEU4OTV4TUeIEYZ_RBFaJ7Ldau9MNzVTNq3w/exec
function doGet(event) {
  return Lib.doGet_doPost(event, "GET");
}

function doPost(event) {
  return Lib.doGet_doPost(event, "POST");
}




function doGet_doPost(event, type) {
 let ret = type === "POST" ? mr_doPost(event) : mr_doGet(event);
 return ContentService.createTextOutput(`${ret}`);
}


function mr_doGet(event) {
  // Logger.log(`doGet ${JSON.stringify(event)}`);
  let mrClassSheetПарсинг = new MrClassSheetПарсинг(getSettings().sheetNames.Парсинг, getContext());
  let objNext = mrClassSheetПарсинг.getNextObjForParse();
  return JSON.stringify(objNext);
}

function mr_doPost(event) {
  Logger.log(`doPost ${JSON.stringify(event)}`);
  if (event.contentLength == -1) {
    return "Поддерживаются только Пост Запросы";
  }

  let ret = "";
  // SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Настройки").appendRow([event.postData.contents]);
  let event_postData_contents = ((json) => { try { return JSON.parse(json) } catch (err) { return undefined } })(event.postData.contents);
  // event_postData_contents;

  Logger.log(`event_postData_contents ${JSON.stringify(event_postData_contents)}`);

  ret = `${ret}\nevent_postData_contents=${JSON.stringify(event_postData_contents)}`
  if (!event_postData_contents) { return ret; }

  mrClassSheetПарсинг = new MrClassSheetПарсинг(getSettings().sheetNames.Парсинг, getContext());
  mrClassSheetПарсинг.saveObjAfterParse(event_postData_contents);
  ret = `OK\n${ret}}`;
  return ret;
  
}



/**
 * https://developers.google.com/apps-script/guides/web
 * When a user visits an app or a program sends the app an HTTP GET request, Apps Script runs the function doGet(e).
 * When a program sends the app an HTTP POST request, Apps Script runs doPost(e) instead.
 * In both cases, the e argument represents an event parameter that can contain information about any request parameters.
 * The structure of the event object is shown in the table below:
 * @typedef {Object} Event
 * @property {string} queryString	- The value of the query string portion of the URL, or null if no query string is specified  // name=alice&n=1&n=2
 * @property {string} parameter	- An object of key/value pairs that correspond to the request parameters. Only the first value is returned for parameters that have multiple values.//  {"name": "alice", "n": "1"}
 * @property {Object} parameters	- An object similar to e.parameter, but with an array of values for each key// {"name": ["alice"], "n": ["1", "2"]}
 * @property {string} contextPath	Not used, always the empty string.
 * @property {namber} contentLength	- The length of the request body for POST requests, or -1 for GET requests // 332
 *
 * @property {Object} postData	- postData
 * @property {namber} postData.length	- The same as e.contentLength // 332
 * @property {string} postData.type	- The MIME type of the POST body // text/csv
 * @property {string} postData.contents	- The content text of the POST body  //  Alice,21
 * @property {string} postData.name	-Always the value "postData"  //  postData

 */














