

$( document ).ready(function() {

    $("#user-table tr").has("td:contains('Archived')").hide();
    
    
    $.expr[":"].contains = $.expr.createPseudo(function(arg) {
    return function( elem ) {
        return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };
});
    
    $("#filter").change(function() {
        var filterVal = $("#filter").val();
        var showArchived = $("#showArchived");
        $("#user-table tr").hide();
        var found = $("tr").has("td:contains('" + filterVal +"')");
        found.show();
        if(!showArchived.is(':checked')){
            $("#user-table tr").has("td:contains('Archived')").hide();
        }
    });
    
    $("#showArchived").change(function() {
        var filterVal = $("#filter").val();
        var showArchived = $("#showArchived");
        $("#user-table tr").hide();
        var found = $("tr").has("td:contains('" + filterVal +"')");
        found.show();
        if(!showArchived.is(':checked')){
            $("#user-table tr").has("td:contains('Archived')").hide();
        }
    });

});