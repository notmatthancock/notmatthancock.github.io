$(document).ready(function() {
    // Add example 1 images
    for (var i = 0; i <= 200; i+=10) {
        img = '<img src="img/example1/' + i + '.png" id="'+i+'" style="display:none; width: 500px" iteration="' + i + '">'
        $('.animation-frames[example=1]').append(img)
    }

    // Add example 1-1 images
    for (var i = 0; i <= 200; i+=10) {
        img = '<img src="img/example1-1/' + i + '.png" id="'+i+'" style="display:none; width: 500px" iteration="' + i + '">'
        $('.animation-frames[example=1-1]').append(img)
    }
 
    // Add example 1-2 images
    for (var i = 0; i <= 250; i+=10) {
        img = '<img src="img/example1-2/' + i + '.png" id="'+i+'" style="display:none; width: 500px" iteration="' + i + '">'
        $('.animation-frames[example=1-2]').append(img)
    }
 
    // Add example 2 images
    for (var i = 0; i <= 250; i+=10) {
        img = '<img src="img/example2/' + i + '.png" id="'+i+'" style="display:none; width: 500px" iteration="' + i + '">'
        $('.animation-frames[example=2]').append(img)
    }

    // Add example 2-ls images
    for (var i = 0; i <= 1500; i+=100) {
        img = '<img src="img/example2-ls/' + i + '.png" id="'+i+'" style="display:none; width: 500px" iteration="' + i + '">'
        $('.animation-frames[example=2-ls]').append(img)
    }

    $('.animation-frames img[iteration=0]').toggle()

    $(document).on('input change', '.animation-frames-controls', function() {
        iter = $(this).val()
        example = $(this).attr('example')
        $('.animation-frames[example=' + example + '] img[iteration!=' + iter +']').hide()
        $('.animation-frames[example=' + example + '] img[iteration='  + iter +']').show()
    })
})
