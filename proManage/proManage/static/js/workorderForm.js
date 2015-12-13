

$( document ).ready(function() {

    
    $("option:contains(Unknown)").text("Open");
    $("option:contains(Yes)").text("Closed");
    $("option:contains(No)").text("Archived");
});