// $(function () {
//             $("#table_atividades").tablesorter();
//          });
//
// $( function() {
//
//   var $table1 = $( '#table_atividades' )
//     .tablesorter({
//       theme : 'blue',
//       // this is the default setting
//       cssChildRow : "tablesorter-childRow",
//
//       // initialize zebra and filter widgets
//       widgets : [ "zebra", "filter", "pager" ],
//
//       widgetOptions: {
//         // output default: '{page}/{totalPages}'
//         // possible variables: {page}, {totalPages}, {filteredPages}, {startRow}, {endRow}, {filteredRows} and {totalRows}
//         pager_output: '{startRow} - {endRow} / {filteredRows} ({totalRows})',
//
//         pager_removeRows: false,
//
//         // include child row content while filtering, if true
//         filter_childRows  : true,
//         // class name applied to filter row and each input
//         filter_cssFilter  : 'tablesorter-filter',
//         // search from beginning
//         filter_startsWith : false,
//         // Set this option to false to make the searches case sensitive
//         filter_ignoreCase : true
//       }
//
//     });
//
//   // hide child rows - get in the habit of not using .hide()
//   // See http://jsfiddle.net/Mottie/u507846y/ & https://github.com/jquery/jquery/issues/1767
//   // and https://github.com/jquery/jquery/issues/2308
//   // This won't be a problem in jQuery v3.0+
//   $table1.find( '.tablesorter-childRow td' ).addClass( 'hidden' );
//
//   // Toggle child row content (td), not hiding the row since we are using rowspan
//   // Using delegate because the pager plugin rebuilds the table after each page change
//   // "delegate" works in jQuery 1.4.2+; use "live" back to v1.3; for older jQuery - SOL
//   $table1.delegate( '.toggle', 'click' ,function() {
//     // use "nextUntil" to toggle multiple child rows
//     // toggle table cells instead of the row
//     $( this )
//       .closest( 'tr' )
//       .nextUntil( 'tr.tablesorter-hasChildRow' )
//       .find( 'td' )
//       .toggleClass( 'hidden' );
//     return false;
//   });
//
//   // Toggle filter_childRows option
//   $( 'button.toggle-combined' ).click( function() {
//     var wo = $table1[0].config.widgetOptions,
//     o = !wo.filter_childRows;
//     wo.filter_childRows = o;
//     $( '.state1' ).html( o.toString() );
//     // update filter; include false parameter to force a new search
//     $table1.trigger( 'search', false );
//     return false;
//   });
//
// });