$("input[value=self]").change(function(e){
    $('form#delivery_address').addClass('hidden')
});

$("input[value=delivery-np]").change(function(e){
    $('p#self-delivery-label').addClass('hidden')
    $('form#delivery_address').removeClass('hidden')

    $('input#id_street').addClass('hidden')

    $('label[for=id_street]').addClass('hidden')
    $('input#id_building_no').addClass('hidden')

    $('label[for=id_building_no]').addClass('hidden')
    $('input#id_building_no').addClass('hidden')

    $('label[for=id_apartments]').addClass('hidden')
    $('input#id_apartments').addClass('hidden')

})

$("input[value=courier-np]").change(function(e){
    $('p#self-delivery-label').addClass('hidden')
    $('form#delivery_address').removeClass('hidden')

    $('input#id_street').removeClass('hidden')
    $('label[for=id_street]').removeClass('hidden')

    $('input#id_building_no').removeClass('hidden')
    $('label[for=id_building_no]').removeClass('hidden')

    $('input#id_apartments').removeClass('hidden')
    $('label[for=id_apartments]').removeClass('hidden')})

    $('input#id_wrh_no').addClass('hidden')
    $('label[for=id_wrh_no]').addClass('hidden')