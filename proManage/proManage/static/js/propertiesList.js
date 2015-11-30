

$( document ).ready(function() {
    $.expr[":"].contains = $.expr.createPseudo(function(arg) {
    return function( elem ) {
        return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };
});
    
    $("#filter").change(function() {
        var filterVal = $("#filter").val();
        $("#user-table tr").hide();
        var found = $("tr").has("td:contains('" + filterVal +"')");
        found.show();
    });

});