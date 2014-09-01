/*jshint strict:false */
/*jslint node: true */
/*jslint browser: true*/
/*global $, jQuery*/
'use strict';


var ajax = (function ($) {
  var sheetUrl = '';
  return {
    setUrl : function (url) {
      sheetUrl = url;
    },
    getTables : function (callback) {
      $.get(list_models_url, function (data) {
        var data1 = data[0];
        return callback(data1);
      });
    },
    get : function (callback) {
      $.get(sheetUrl, function (data) {
        return callback(data);
      });
    },
    post : function (data, callback) {
      $.post(sheetUrl, data, function (data) {
        return callback(data);
      });
    },
    patch : function (id, data, callback, errback) {
      // data.csrfmiddlewaretoken = csrf_token
      $.ajax({
        headers : {
          'Accept' : 'application/json',
          'Content-Type' : 'application/json'
        },
        url : sheetUrl + id,
        type : 'PATCH',
        data : JSON.stringify(data),
        success : function () {
          return callback();
        },
        error : function () {
          return errback();
        }
      });
    }
  };
}(jQuery, {}));


var SheetTable = function () {
  this.sheet_schema = null;
  this.sheet_name = null;
  this.table = null;
};

SheetTable.prototype.setTableData = function (sheet_schema, sheet_name) {
  this.sheet_schema = sheet_schema;
  this.sheet_name = sheet_name;
};

SheetTable.prototype.get_ajax_data = function () {
  var self = this;
  ajax.get(function (data) {
    self.create(data);
  });
};

SheetTable.prototype.prepHtml = function () {
  $("#sheet_field>div").remove();
  $("#object_form>div").remove();
  $("#sheet_field").append('<div/>');
  $("#object_form").append('<div/>');
  $("#object_form>div").append('<p/>');
  $("#object_form").css("border", "inset 2px #a5a4a4");
  $("#object_form>div>p").text(this.sheet_name +' добавить:');
  $("#sheet_field>div").unbind().find('table').remove();
  $("#sheet_field>div").append('<table/>');
};

SheetTable.prototype.getDataSet = function (table_data) {
  var self = this;
  var dataSet = [];
  var dataRow = [];
  _.each(table_data , function( row, index, data ) {
      dataRow = [];
      _.each(self.sheet_schema , function( column, index, sheet_schema ) {
        dataRow.push(row[column.id]);
      });
      dataSet.push(dataRow);
  });
  return dataSet;
};

SheetTable.prototype.showForm = function (dataSet, validator) {
  var self = this;
  $('#object_form>div').append(
      '<form id="addRowForm" input type="submit" value="Submit" action="">' +
      '</form>'
    );
  _.each(self.sheet_schema , function (column, index, sheet_schema) {
    if (column.id != 'id') {
      $('#object_form>div>form').append(
          '<p class="">' +
          '<label for="'+ column.id + '">'+ column.name +
          '<input type="text" id="' + column.id + '" size="20"' +
            'class="' + column.type +'"' +
            'name="' + column.id + '"' +
            'value="" placeholder="" />' +
          '</p>'
        );
    }
    if (column.type === 'Date') {
      $('#object_form>div>form #'+ column.id).datepicker({
        dateFormat: 'dd/mm/yy'
      });
    }
  });
  $('#object_form>div>form').append('<input type="submit" value="Submit" action="">');
  $('#addRowForm').submit(function () {
    var values = {};
    var form_valid = true;
    $.each($('#addRowForm').serializeArray(), function(i, field) {
        form_valid &= validator.validate($('#addRowForm #'+field.name), field.value);
        if ($('#addRowForm #'+field.name).is('.Integer')) {
          values[field.name] = +field.value;
        } else if ($('#addRowForm #'+field.name).is('.Date')) {
          // dd/mm/yyyy -> yyyy-mm-dd
          values[field.name] = field.value.replace(
            new RegExp("^(\\d{2}).\(\\d{2}).\(\\d{4})$"), "$3-$2-$1");
        } else {
          values[field.name] = field.value;
        }
    });
    if (form_valid) {
      ajax.post(values, function (data) {
          var dataSet = self.getDataSet([data]);
          self.drawRow(dataSet[0]);
      } );
    }
    return false;
  });
};

SheetTable.prototype.drawRow = function (row) {
  this.table.row.add( row ).draw();
};

SheetTable.prototype.getColumnId = function () {
  var self = this;
  var Columns = [];
  _.each(self.sheet_schema , function (column, index, sheet_schema) {
        Columns.push(column.id);
  });
  return Columns;
};

SheetTable.prototype.showTable = function (dataSet) {
  var self = this
  var Columns = [];
  var aoColumns = []
  _.each(self.sheet_schema , function (column, index, sheet_schema) {
      Columns.push({ "title": column.name });
      if (column.type == "Date") {
        aoColumns.push({ "sClass": "Date ", "sTitle": column.name });
      } else if (column.type == "Integer") {
        aoColumns.push({ "sClass": "Integer ", "sTitle": column.name });
      } else if (column.type == "Char") {
        aoColumns.push({ "sClass": "Char ", "sTitle": column.name });
      } else if (column.type == "Auto") {
        aoColumns.push({ "sClass": "ID ", "sTitle": column.name });
      } else {
        aoColumns.push({ "sTitle": column.name });
      }
  });
  $('#sheet_field>table')
    .html( '<table' +
        'cellpadding="0" cellspacing="0" border="0"' +
        'class="display" id="example">' +
        '</table>'
      );
  var table = $('#sheet_field>div>table').DataTable( {
      "data": dataSet,
      "columns": Columns,
      "aoColumns": aoColumns,
      //"bAutoWidth": false,
      "bPaginate": false,
      "bFilter": false,
      "bSort" : false,
      "bInfo": false,
      "oLanguage": {
        "sEmptyTable": "Таблица пуста"
      },
      "aLengthMenu": [[-1, 10, 25, 50, 100, 200 ],
                    ["All", 10, 25, 50, 100, 200 ]]
  });
  self.table = table;
  return table;
};

SheetTable.prototype.setupTableHeaders = function () {
  $('#sheet_field>div thead').find('.ID').removeClass('ID');
  $('#sheet_field>div thead').find('.Integer').removeClass('Integer');
  $('#sheet_field>div thead').find('.Char').removeClass('Char');
  $('#sheet_field>div thead').find('.Date').removeClass('Date');
};

SheetTable.prototype.createEventsForCells = function (validator, columnsId) {
  
  $('#sheet_field>div>').on('click', function (event) {

    var target = $( event.target );

    if (target.is('.Date') ) {
      tableElementManager.editCell(target,
          validator,
          tableElementManager.appendDatepickerElement,
          columnsId
        );  
    }
    else if (target.is('.Char') ) {
      tableElementManager.editCell(target,
          validator,
          tableElementManager.appendInputElement,
          columnsId
        );
    }
    else if (target.is('.Integer') ) {
      tableElementManager.editCell(target,
          validator,
          tableElementManager.appendInputElement,
          columnsId
        );
    }
    else {
      tableElementManager.saveInput(columnsId, validator);
    }
  });
};

SheetTable.prototype.create = function (data) {
  this.prepHtml();
  var validator = new Vadidator(
      new RegExp("^\\d{2}/\\d{2}/\\d{4}$"),
      new RegExp("^\\d{1,15}$"),
      new RegExp("^[a-zA-Zа-яА-Я]{1,99}$")
    );
  var dataSet = this.getDataSet(data);
  this.showTable(dataSet);
  this.showForm(dataSet, validator);
  var columnsId = this.getColumnId();
  this.setupTableHeaders();
  this.createEventsForCells(validator, columnsId);
};

var Vadidator = function (date, integer, char) {
  this.date = date;
  this.integer = integer;
  this.char = char;
};

Vadidator.prototype.validate = function ($cell, value) {
  var reg_patt;
  if ($cell.is('.Char')) {
    reg_patt = this.char;
  } else if ($cell.is('.Integer')) {
    reg_patt = this.integer;
  } else if ($cell.is('.Date')) {
    reg_patt = this.date;
  } else {
    return false;
  }
  if (reg_patt.test(value)) {
    return true;
  } else {
    return false;
  }
};

var tableElementManager = {

  appendInputElement : function ($cell, p_scnt) {
    $cell.append(
      '<p class="edit">' +
        '<label class=edit for="p_scnts">' +
        '<input type="text" id="p_scnt" class="edit" size="20"' +
          'name="' + p_scnt + '_' + '"' +
          'value="'+ $cell.attr('data-value') +'" placeholder="" />' +
      '</p>'
    )
    return $('#p_scnt')
  },

  appendDatepickerElement : function ($cell, p_scnt) {
    var $date_input = tableElementManager.appendInputElement($cell)
    $(p_scnt).datepicker({
      dateFormat: 'dd/mm/yy',
    });
  },

  editCell : function ($cell, validator, input_field, columnsId) {
    tableElementManager.saveInput(columnsId, validator);
    $cell.attr('data-value', $cell.text());
    $cell.addClass('edit-hidden').text('');
    input_field($cell, "#p_scnt");
    $(".edit").on('click', function (e) {
      return false;
    });
    $("#p_scnt").focus().val($cell.attr('data-value'));
    return false;
  },

  hideInput : function ($cell, value) {
    $cell.text(value);
    $cell.removeClass('edit-hidden');
    $cell.removeAttr('data-value');
  },

  saveInput : function (columnsId, validator) {
    $('.edit-hidden').each( function( index ) {
      var $cell = $(this)
      var newValue = $cell.find('#p_scnt')[0].value;
      var oldValue = $cell.attr('data-value');
      if (newValue != oldValue && validator.validate($cell, newValue)) {
        var data = {}
        if ($cell.is('.Date')) {
          data[columnsId[$(this).index()]] = newValue.replace(
            new RegExp("^(\\d{2}).\(\\d{2}).\(\\d{4})$"), "$3-$2-$1");
        } else {
          data[columnsId[$(this).index()]] = newValue          
        }
        ajax.patch(
          $cell.parent().children('.ID').text(),
          data,
          function () {
            tableElementManager.hideInput($cell, newValue);          },
          function () {
            tableElementManager.hideInput($cell, oldValue);
          }
        );
      } else {
        tableElementManager.hideInput($cell, oldValue);
      };
    });
    $('#datapicker').each( function (index) {
      $(this).remove()
    });
    return false;
  },
};

var SheetTableSingleton = (function () {
  var instance;
  function createInstance() {
    var object = new SheetTable();
    return object;
  }
  return {
    getInstance: function () {
      if (!instance) {
        instance = createInstance();
      }
      return instance;
    }
  };
})();

var SheetList = function () {
};

SheetList.prototype.hire = function () {
  ajax.getTables(function (data) {
    $("#sheet_name").unbind().find('div').remove();
    _.each(data, function (element, index, sheets) {
      $("#sheet_name").append('<div/>');
      $("#sheet_name>div").last()
        .append(element.sheet)
        .on('click', function (e) {
          ajax.setUrl(element.url)
          $('.strong').each( function (index) {
            $(this).removeClass('strong');
          } );
          $(this).addClass('strong');
          var sheetTable = SheetTableSingleton.getInstance();
          sheetTable.setTableData(element.fields, element.sheet);
          sheetTable.get_ajax_data();
          return
        });
    });
  });
};


$( document ).ready(function () {
  var sheetList = new SheetList();
  sheetList.hire();
});