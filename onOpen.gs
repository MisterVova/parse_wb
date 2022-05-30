function onOpen() {

  var ui = SpreadsheetApp.getUi();
  var menu = ui.createMenu("Доп.Меню");
  menu.addSubMenu(SpreadsheetApp.getUi().createMenu('Парсинг')
    .addItem('Добавить выбранное', 'menu_Добавить_выбранное')
    //   .addItem('На Печать', 'menu_print')
    //   .addItem('Пропустить', 'menu_skip')
    //   .addItem('Выполнено', 'menu_done')
    //   .addItem('Следующий', 'menu_next')
  );

  // menu.addSubMenu(SpreadsheetApp.getUi().createMenu('История упаковки')
  //   .addItem('Обновить', 'menuИмпортДанных')
  //   .addItem('Очистить Консоли', 'menuОчиститьКонсоли')
  // );

  // menu.addSubMenu(get_menu_WB());
  menu.addToUi();
  Logger.log(`onOpen.onOpen() menu заданно `);
}

function menu_Добавить_выбранное() {
  let add_keys = new Array();
  SpreadsheetApp.getSelection()
  var activeSheet = SpreadsheetApp.getActiveSheet();
  // var rangeList = activeSheet.getRangeList(['A1:B4', 'D1:E4']);
  // rangeList.activate();

  var selection = activeSheet.getSelection();
  // Current Cell: D1
  Logger.log('Current Cell: ' + selection.getCurrentCell().getA1Notation());
  // Active Range: D1:E4
  Logger.log('Active Range: ' + selection.getActiveRange().getA1Notation());
  // Active Ranges: A1:B4, D1:E4
  var ranges = selection.getActiveRangeList().getRanges();
  for (var i = 0; i < ranges.length; i++) {
    Logger.log('Active Ranges: ' + ranges[i].getA1Notation());
    let vls = ranges[i].getValues().flat();
    add_keys = [].concat(add_keys, vls)
  }
  Logger.log('Active Sheet: ' + selection.getActiveSheet().getName());
  add_keys = add_keys.filter((v, i, arr) => { return `${v}` != "" })

  Logger.log('vls_add ' + add_keys.length);
  Logger.log('vls_add ' + add_keys);

  let mrClassSheetПарсинг = new  MrClassSheetПарсинг(getSettings().sheetNames.Парсинг, getContext());
  mrClassSheetПарсинг.add_new_keys(add_keys);
}










