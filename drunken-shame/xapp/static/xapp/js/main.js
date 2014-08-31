var ajax = (function () {
  var _url = '';
  return {
    set_url : function( url ) {
      _url = url;
    },
    get_tables : function(callback) {
      $.get( list_models_url, function( data ) {
        var data1 = data[0];
        return callback(data1)
      } );
    },
    get : function(callback) {
      $.get( _url, function( data ) {
        return callback(data)
      } );
    },
    post : function(id, data, callback) {
      data.csrfmiddlewaretoken = csrf_token
      JSON.stringify(data)
      $.post(_url, data)
      return callback
    },
    patch : function(id, data, callback) {
      data.csrfmiddlewaretoken = csrf_token
      JSON.stringify(data)
      $.patch(_url+id, data)
      return callback
    }
  };
}());



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

var SheetTable = function ( ) {
  this.sheet_schema = null;
  this.sheet_name = null;
};

SheetTable.prototype.setTableData = function ( sheet_schema, sheet_name ) {
  this.sheet_schema = sheet_schema;
  this.sheet_name = sheet_name;
};

SheetTable.prototype.get_ajax_data = function() {
  ajax.get(function( data ) {
    sheetTable.create(data);
  } );
};

SheetTable.prototype.prepHtml = function() {
  $("#sheet_field>div").remove();
  $("#object_form>div").remove();
  $("#sheet_field").append('<div/>');
  $("#object_form").append('<div/>');
  $("#object_form>div").append('<p/>');
  $("#object_form").css("border", "inset 2px #a5a4a4");
  $("#object_form>div>p").text(this.sheet_name+' добавить:');
  $("#sheet_field>div").unbind().find('table').remove();
  $("#sheet_field>div").append('<table/>');
}

SheetTable.prototype.getDataSet = function( table_data ) {
  self = this
  var dataSet = [];
  var dataRow = [];

  _.each(table_data , function( row, index, data ) {
      dataRow = [];
      _.each(self.sheet_schema , function( column, index, sheet_schema ) {
          dataRow.push(row[column.id]);
      });
      dataSet.push(dataRow);
  } );
  return dataSet;
}

SheetTable.prototype.showForm = function( dataSet ) {
  self = this
  $('#object_form>div').append('<form action="" input type="submit" value="Submit"></form>');
  _.each(self.sheet_schema , function( column, index, sheet_schema ) {
      $('#object_form>div>form').append(
          '<p class="">' +
          '<label for="'+ column.id + '">'+ column.name +
          '<input type="text" id="' + column.id + '" size="20"' +
            'name="' + column.name + '"' +
            'value="" placeholder="" />' +
          '</p>'
      );
  } );
  $('#object_form>div>form').append('<input type="submit" value="Submit">');
};

SheetTable.prototype.showTable = function( dataSet ) {
  self = this
  var Columns = [];
  var aoColumns = []
  _.each(self.sheet_schema , function( column, index, sheet_schema ) {
      Columns.push({ "title": column.name });
      if (column.type == "Date") {
        aoColumns.push({ "sClass": "Date ", "sTitle": column.name, });
      } else if (column.type == "Integer") {
        aoColumns.push({ "sClass": "Integer ", "sTitle": column.name, });
      } else if (column.type == "Char") {
        aoColumns.push({ "sClass": "Char ", "sTitle": column.name, });
      } else {
        aoColumns.push({ "sTitle": column.name, });
      };
  } );
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
      "aLengthMenu": [[-1, 10, 25, 50, 100, 200, ],
                    ["All", 10, 25, 50, 100, 200, ]],
  } );
}


SheetTable.prototype.addRow = function( ) {
  $('#sheet_field>div').on( 'addRow', function ( event ) {
    var row = Array.prototype.slice.call(arguments).slice(1);
    table.row.add( row ).draw();
    $('.Date').off('click')
    $('.Date').on('click', function (e) {
      editDateCell($(this));
    } );
    $('.Char').each( function( index ) {
      editCell($(this), new RegExp("^\\w{1,99}$"));
    } );
    $('.Integer').each( function( index ) {
      editCell($(this), new RegExp("^\\d{1,15}$"));
    } );
  } );
}

SheetTable.prototype.setupTableHeaders = function( ) {
  $('#sheet_field>div thead').find('.ID').removeClass('ID');
  $('#sheet_field>div thead').find('.Integer').removeClass('Integer');
  $('#sheet_field>div thead').find('.Char').removeClass('Char');
  $('#sheet_field>div thead').find('.Date').removeClass('Date');
}

SheetTable.prototype.createEventsForCells = function( ) {
  validator = new Vadidator(
    new RegExp("^\\d{2}/\\d{2}/\\d{4}$"),
    new RegExp("^\\d{1,15}$"),
    new RegExp("^\\w{1,99}$")
  );
  $('#sheet_field>div>').on('click', function (event) {

    var target = $( event.target );

    if (target.is('.Date') ) {
      tableElementManager.editCell(target,
        validator,
        tableElementManager.appendDatepickerElement );  
    }
    else if (target.is('.Char') ) {
      tableElementManager.editCell(target,
        validator,
        tableElementManager.appendInputElement);
    }
    else if (target.is('.Integer') ) {
      tableElementManager.editCell(target,
        validator,
        tableElementManager.appendInputElement);
    }
    else {
      tableElementManager.hideInput();
    }
  } );

  // $('#object_form>div').click(function() {
  //   createRecord()
  //   return false;
  // } );
}

SheetTable.prototype.create = function( data ) {
  this.prepHtml();
  var dataSet = this.getDataSet(data);
  this.showTable(dataSet, this.sheet_schema);
  this.showForm(dataSet, this.sheet_schema);
  this.addRow();
  this.setupTableHeaders();
  this.createEventsForCells();
};

Vadidator = function ( date, integer, char ) {
  this.date = date;
  this.integer = integer;
  this.char = char;
}

Vadidator.prototype.validate = function ($cell) {
  if ($cell.is('.Char')) {
    reg_patt = this.char;
  } else if ($cell.is('.Integer')) {
    reg_patt = this.integer;
  } else if ($cell.is('.Date')) {
    reg_patt = this.date;
  } else {
    return false;
  }
  if (reg_patt.test($cell.find('#p_scnt')[0].value)) {
    return true;
  } else {
    return false;
  }
}

tableElementManager = {

  appendInputElement : function ($cell) {
    $cell.append(
      '<p class="edit">' +
        '<label class=edit for="p_scnts">' +
        '<input type="text" id="p_scnt" class="edit" size="20"' +
          'name="p_scnt_' + '"' +
          'value="'+ $cell.attr('data-value') +'" placeholder="" />' +
      '</p>'
    )
    return $('#p_scnt')
  },

  appendDatepickerElement : function ($cell) {
    $date_input = tableElementManager.appendInputElement($cell)
    $("#p_scnt").datepicker({
      dateFormat: 'dd/mm/yy',
    } );
  },

  editCell : function ($cell, validator, input_type) {
    tableElementManager.hideInput();
    $cell.attr('data-value', $cell.text());
    $cell.addClass('edit-hidden').text('');
    input_type($cell);
    $(".edit").on('click', function (e) {
      return false;
    } );
    $("#p_scnt").focus().val($cell.attr('data-value'));
    return false;
  },

  hideInput : function () {
    $('.edit-hidden').each( function( index ) {
      if (validator.validate($(this))) {
        $(this).attr('data-value', $(this).find('#p_scnt')[0].value);
      };
      $(this).text($(this).attr('data-value'));
      $(this).removeClass('edit-hidden');
    } );
    $('#datapicker').each( function( index ) {
      $(this).remove()
    } );
    return false;
  },

}

createRecord = function (data) {
  data = data || {
    "date_joined": "2014-01-01",
    "name": "a",
    "paycheck": 123
  };
  return false;
}




var SheetList = function ( ) {
};

SheetList.prototype.hire = function() {
  ajax.get_tables(function( data ) {
    $("#sheet_name").unbind().find('div').remove();
    _.each(data, function(element, index, sheets) {
      $("#sheet_name").append('<div/>');
      $("#sheet_name>div").last()
        .append(element.sheet)
        .on('click', function(e) {
          ajax.set_url(element.url)
          $('.strong').each( function( index ) {
            $(this).removeClass('strong');
          } );
          $(this).addClass('strong');
          sheetTable = SheetTableSingleton.getInstance();
          sheetTable.setTableData(element.fields, element.sheet);
          sheetTable.get_ajax_data();
          return
        } );
    } );
  } );
};







$( document ).ready(function() {
  var sheetList = new SheetList();
  sheetList.hire();
} );