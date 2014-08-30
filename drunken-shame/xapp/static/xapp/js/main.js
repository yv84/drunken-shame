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
        var data1 = data[0];
        return callback(data1)
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



var SheetTable = function ( ) {
};

SheetTable.prototype.get_ajax_data = function( sheet_schema, url, sheet_name ) {
  $.get(url, function( data ) {
    sheetTable.create(sheet_schema, data, sheet_name);
  } );
};

SheetTable.prototype.prepHtml = function( sheet_name ) {
  $("#sheet_field>div").remove();
  $("#object_form>div").remove();
  $("#sheet_field").append('<div/>');
  $("#object_form").append('<div/>');
  $("#object_form>div").append('<p/>');
  $("#object_form").css("border", "inset 2px #a5a4a4");
  $("#object_form>div>p").text(sheet_name+' добавить:');
  $("#sheet_field>div").unbind().find('table').remove();
  $("#sheet_field>div").append('<table/>');
}

SheetTable.prototype.getDataSet = function( sheet_schema, table_data ) {
  var dataSet = [];
  var dataRow = [];

  _.each(table_data , function( row, index, data ) {
      dataRow = [];
      _.each(sheet_schema , function( column, index, sheet_schema ) {
          dataRow.push(row[column.id]);
      });
      dataSet.push(dataRow);
  } );
  return dataSet;
}

SheetTable.prototype.showTable = function( dataSet, sheet_schema ) {
  var Columns = [];
  var aoColumns = []
  $('#object_form>div').append('<form action="" input type="submit" value="Submit"></form>');
  _.each(sheet_schema , function( column, index, sheet_schema ) {
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
  $('.Date').on('click', function (e) {
    editDateCell($(this));
  } );
  $('.Char').each( function( index ) {
    editCell($(this), new RegExp("^\\w{1,99}$"));
  } );
  $('.Integer').each( function( index ) {
    editCell($(this), new RegExp("^\\d{1,15}$"));
  } );
  $('#object_form>div').click(function() {
    createRecord()
    return false;
  } );
}

SheetTable.prototype.create = function( sheet_schema, data, sheet_name ) {
  this.prepHtml(sheet_name);
  var dataSet = this.getDataSet(sheet_schema, data);
  this.showTable(dataSet, sheet_schema);
  this.addRow();
  this.setupTableHeaders();
  this.createEventsForCells();
};










var InputElement = function ( ) {

};

InputElement.prototype.show = function ( ) {

};

InputElement.prototype.hide = function ( ) {

};








editCell = function (cell, reg_patt) {
  cell.one('click', function (e) {
    $('.hasDatepicker').each( function( index ) {
      $(this).remove();
    } );
    $('.edit-hidden').each( function( index ) {
      $(this).text($(this).attr('data-value'));
      editCell($(this), reg_patt);
      $(this).removeClass('edit-hidden');
    });
    $(this).attr('data-value', $(this).text());
    $(this).addClass('edit-hidden').text('');
    $(this).append(
        '<p class="edit">' +
        '<label class=edit for="p_scnts">' +
        '<input type="text" id="p_scnt" class="edit" size="20"' +
          'name="p_scnt_' + '"' +
          'value="'+ $(this).attr('data-value') +'" placeholder="" />' +
        '</label> <a href="#" id="okScnt">Ok</a>' +
        '</label> <a href="#" id="remScnt">Отмена</a>' +
        '</p>'
    );
    $(this).unbind();
    $(".edit").on('click', function (e) {
      return false;
    } );
    $("#okScnt").on('click', function (e) {
      if (reg_patt.test($(cell).find('#p_scnt')[0].value)){
          saveInput(cell, reg_patt);
      }
      return false;
    } );
    $("#p_scnt").focus().val($(this).attr('data-value'));;
    setTimeout(function() {
      $("body :not(.Integer, .Char, .edit)").on('click', function (e) {
        hideInput($(this), reg_patt);
        return true;
      } );
    }, 200);
    return false;
  } );
};
saveInput = function (cell, reg_patt) {
  $('.edit-hidden').each( function( index ) {
    $(this).text($(cell).find('#p_scnt')[0].value);
    editCell($(this), reg_patt);
    $(this).removeClass('edit-hidden');
  } );
  return false;
};
hideInput = function (cell, reg_patt) {
  $('.edit-hidden').each( function( index ) {
    $(this).text($(this).attr('data-value'));
    editCell($(this), reg_patt);
    $(this).removeClass('edit-hidden');
  } );
  return false;
};

editDateCell = function (cell) {
    $('#datapicker').each( function( index ) {
      $(this).remove()
    } );
    cell.append('<div class="hasDatepicker">' +
                  '<div id="datapicker"></div>' +
                '</div>'
    );
    $("#datapicker").datepicker({
      dateFormat: 'dd/mm/yy',
      onSelect: function(dateText, inst) {
          cell.text(dateText);
          $("body").trigger('click');
      }
    } );
    setTimeout(function() {
      $("body").one("click", function (e) {
        $('.hasDatepicker').each( function( index ) {
          $(this).remove();
        } );
        return true;
      } );
    }, 200);
};


createRecord = function (data) {
  data = data || {
    "date_joined": "2014-01-01",
    "name": "a",
    "paycheck": 123
  };
  return false;
}




var SheetList = function ( ) {
  sheetTable = new SheetTable();
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
          return sheetTable.get_ajax_data(element.fields, element.url, element.sheet);
        } );
    } );
  } );
};







$( document ).ready(function() {
  var sheetList = new SheetList();
  sheetList.hire();
} );