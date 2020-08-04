$("input[id='exampleRadios1']").change(function(e){
    $('form#delivery-np').addClass('hidden')
    $('form#courier-np').addClass('hidden')
});

$("input[id='exampleRadios2']").change(function(e){
    $('form#delivery-np').removeClass('hidden')
    $('form#courier-np').addClass('hidden')
});

$("input[id='exampleRadios3']").change(function(e){
    $('form#delivery-np').addClass('hidden')
    $('form#courier-np').removeClass('hidden')
});