$(function() {
    var g_func = "x*x - y*y - 0.11";
    var h_func = "2*x*y + 0.6557";

    canvas  = $('#js-frac')[0]
    s = 0; $('body > :not(#js-frac)').each(function() { s+=$(this).outerHeight(true); })
    canvas.width  = $(window).height() - s + 80
    canvas.height = $(window).height() - s + 80 
    context = canvas.getContext('2d');

    // fractal container object
    frac = {
        f: "( function(x) { return [x[0]*x[0]-x[1]*x[1] - 0.11, 2* x[0]*x[1] + 0.6557 ] } )",
        con_limit: 200,
        div_limit: 10,
        
        width:  canvas.width,
        height: canvas.height,
        
        xMin: -1.0,
        xMax: 1.0,
        xStep: 2.0 / (canvas.width-1),

        yMin: -1.0,
        yMax: 1.0,
        yStep: 2.0 / (canvas.height-1),

        hues: [0, 204, 62],

        // This array stores the number of iterations a point
        // 'survives' the functional iteration.
        points: new Uint16Array(canvas.width*canvas.height),

        // worker communication flag
        color_only: false
    };

    var worker = "this string means nothing"; // initialize
    function make_worker() {
        worker = new Worker('./make-frac.js');
        $('#frac-loading').html('');

        worker.addEventListener('message', function(msg) {
            switch ( msg.data.topic ) {
                case 'testing':
                    // The message is a status update on the percent completion of point testing.
                    var pc = parseFloat(msg.data.iter);
                    pc = Math.round( ((pc+1) / frac.width)*100 ) 
                    $('#frac-loading').html( 'Testing points: ' + pc + '%' );
                    break;
                case 'frac':
                    // Recieving updated frac object.
                    frac = JSON.parse( msg.data.frac )
                    $('#frac-loading').html('');
                    if ( $('#draw').css('display') == 'none' )
                        $('#draw, #stop').toggle();
                    break;
                case 'image_data':
                    id = new ImageData(frac.width, frac.height);
                    id.data.set(msg.data.image_data);
                    context.putImageData(id, 0, 0)
                    break;
                default:
                    throw 'Incoming message had no topic.';
            }

        }, false);
    };
    make_worker();
    worker.postMessage( JSON.stringify(frac) );

    // DOM init stuff / event responders.
    $('input.xMin').val( frac.xMin );
    $('input.xMax').val( frac.xMax );
    $('input.yMin').val( frac.yMin );
    $('input.yMax').val( frac.yMax );
    $('#g_func').val( g_func );
    $('#h_func').val( h_func );
    $('#convergence_limit').val( frac.con_limit );
    $('#divergence_limit').val( frac.div_limit );
    $('#canvas_width').val( frac.width );
    $('#canvas_height').val( frac.height );
    // set palette box colors
    for(var j=1; j<=3; j+=1) {
        $('.color-palette[which='+String(j)+']').css('background-color', 'hsl('+frac.hues[j-1]+',100%,50%)');
        var changer = '<div class="hue-changer" which="'+j+'"><input type="range" min="0" max="360" step="1"';
        changer += ' value="'+frac.hues[j-1]+'"></div>';
        $('body').append( changer )
    }

    $('body').on('click', '.color-palette', function() {
        var w = $(this).attr('which');
        var t = $(this).position().top - 30;
        var l = $(this).position().left - 150 - 5;
        $('.hue-changer[which='+w+']').css({left: l, top: t}).show();
        $('.hue-changer[which='+w+'] > input').focus()
    });

    $('body').on('input change', '.hue-changer > input', function() {
        $('.color-palette[which='+$(this).parent().attr('which')+']').css('background-color', 'hsl('+parseInt($(this).val())+',100%,50%)');
        frac.hues[ $(this).parent().attr('which')-1 ] = parseInt($(this).val())
    });

    $('body').on('focusout', '.hue-changer > input', function(e) {
        $(this).parent().hide()
    });
	
    // Error checking for integer inputs.
    $('body').on('change', '.integer-input', function() {
        if ( isNaN( $(this).val() ) ) {
            var tmpval = this.id.startsWith('canvas') ? 600 : 100;
            $(this).val(tmpval);
            alert('Invalid input. Value set to '+tmpval+' for the time being.');
        }
        else { // all good, but set to integer in case float was entered.
            $(this).val( parseInt($(this).val()) );
        }
    });

    $('body').on('change', 'input.xMin, input.xMax, input.yMin, input.yMax', function() {
        if ( isNaN( $(this).val() ) ) {
            alert('Non-number enter for mathematical bound.');
            $('input.'+$(this).attr('class')).val( ($(this).attr('class').endsWith('Max')) ? 1 : -1 )
        }
        $('input.'+$(this).attr('class')).val( $(this).val() );
    });

    $('body').on('click', '#stop', function() {
        worker.terminate();
        make_worker();
        $('#draw, #stop').toggle();
    });

    $('body').on('click', '#draw', function() {
        update_frac(); 
        $('#draw, #stop').toggle()
        if (!stop) worker.postMessage(JSON.stringify(frac));
    });

    $('body').on('click', '#recolor', function() {
        frac.color_only = true;
        worker.postMessage(JSON.stringify(frac));
    });

    var stop = false; 
    update_frac = function() {
        // Set the convergence and divergence limits from values.
        frac.con_limit = parseInt( $('#convergence_limit').val() );
        frac.div_limit = parseInt( $('#divergence_limit').val() );

        // Set canvas width and height as well as frac object data.
        $('#js-frac')[0].width = parseInt( $('#canvas_width').val() );
        $('#js-frac')[0].height = parseInt( $('#canvas_height').val() );
        frac.width = parseInt( $('#js-frac').width() );
        frac.height = parseInt( $('#js-frac').height() );

        // Set the limits of the mathematical region of the canvas.
        frac.xMin = parseFloat( $('#frac-table input.xMin:first').val() );
        frac.xMax = parseFloat( $('#frac-table input.xMax:first').val() );
        frac.yMin = parseFloat( $('#frac-table input.yMin:first').val() );
        frac.yMax = parseFloat( $('#frac-table input.yMax:first').val() );
        
        // Set the resolution of the canvas.
        frac.xStep = ( frac.xMax - frac.xMin ) / (frac.width - 1);
        frac.yStep = ( frac.yMax - frac.yMin ) / (frac.height - 1);
        
        // Now we build the vector valued function, f, to be iterated
        // from the two inputs from the dom.
        f = "( function(x) { return [";
        // the last replacement here is a workaround for the 'x' getting replaced in 'exp'.
        f += $('#g_func').val().replace(/x/g,'x[0]').replace(/y/g,'x[1]').replace(/ex\[0\]p/g,'exp') + ",";
        f += $('#h_func').val().replace(/x/g,'x[0]').replace(/y/g,'x[1]').replace(/ex\[0\]p/g,'exp');
        f += "]; } )";

        // Next, we do a try/catch of an eval of the function to test it for errors,
        // and set the stop flag to true to prevent the worker from proceeding.
        stop = false;
        try {
            eval( f )([0,0]);
        } catch ( e ) {
            if ( e instanceof SyntaxError )
                alert( "There was a syntax error in one of the functions." );
            if ( e instanceof ReferenceError )
                alert( "Reference error. Did you forget \"Math.\" before a math function?" );
            stop = true;
        }
        if ( !stop ) frac.f = f; 
    }

});
