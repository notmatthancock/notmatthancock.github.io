var origin = [0,0];
var pclass = [0, null, 1];
var labels = ['&#9679;', null, '&#9632;'];
 points = Array();
var pid = 0;

// Return the html string to be added, and add the
// point to the point list (after converting to mathematical coords).
add_point = function(t, l, w) {
    if (w != 0 && w != 2) {
        console.error('Click code not 0 or 2. Probably a browser compatibility issue.')
        return false;
    }

    // Convert to math coords.
    var mathx = parseInt(l-origin[0]);
    var mathy = parseInt(origin[1]-t);

    //l = mathx + origin[0];
    //t = origin[1] - mathy

    // Add the point to the list.
    points.push([pid, mathx, mathy, pclass[w]])

    // Plot the point to the screen.
    $('#pgrid').append('<div id="'+pid+'" class="point class'+pclass[w]+'" style="left: '+(l-10)+'px; top: '+(t-10)+'px;"></div>')

    // Increment the id counter.
    pid += 1;
}

points_empty = function() {
    if (points.length == 0) {
        alert('You haven\'t added any points, yet.')
        return true;
    }
    else {
        return false;
    }
}

$(document).ready(function() {
    // Initialize the main table.
    //var pad = 2*$('h1').outerHeight(true);
    //$('#ptable').height($(window).height() - pad);
    //$('#wrapper, #ptable').width( $(window).width() - pad);

    // Draw x and y axes.
    origin[0] = $('#pgrid').outerWidth()*0.5-1.5;
    origin[1] = $('#pgrid').outerHeight()*0.5-1.5;
    $('#pgrid').append('<div class="axes x-axis" style="left: 0; top: '+origin[1]+'px;"></div>');
    $('#pgrid').append('<div class="axes y-axis" style="top: 0; left: '+origin[0]+'px;"></div>');

    // Add points if they are provided from a share url.
    if (location.hash != '') {
        pid = 0;
        points = Array();
        $('div.point').remove();
         pstring = decodeURIComponent(location.hash.slice(1)).split(',');

        // Check if the share url is valid.
        if (pstring.length % 3 !=0) {
            console.error("Invalid share hash.")
            location.hash = "";
        }
        else {
            for(var i=0; i < pstring.length/3; i+=1) {
                add_point(parseInt(origin[1]-pstring[3*i+1]),
                          parseInt(pstring[3*i])+origin[0],
                          (pstring[3*i+2] == '0') ? 0 : 2);
            }
        }
    }

    // Remove point event.
    $('#pgrid').on('mousedown', 'div.point', function(ev) { 
        if ($('#share-url').is(':focus')) {
            $('#share-url').remove();
        }
        else {
            $('div.point#'+this.id).remove();
            var id = parseInt(this.id);
            for(var i=0; i < points.length; i+=1) {
                if (points[i][0] == id) {
                    points.splice(i, 1);
                    break;
                }
            }
        }

        // Protect against double events from grid clicks.
        ev.stopPropagation();
    });

    // Add point event / disable right-click menu on grid.
    $('#pgrid').contextmenu(function() { return false; })
    $('#ptable').on('mousedown', '#pgrid', function(ev) {
        if ($('#share-url').is(':focus')) {
            $('#share-url').remove();
            return;
        }
        else {
            var pT = parseInt(ev.pageY-$(this).offset().top);
            var pL = parseInt(ev.pageX-$(this).offset().left);
            add_point(pT, pL, ev.button);
        }

        // Protect against double events from point clicks.
        ev.stopPropagation()
        return false;
    });

    // Show coordinates in side menu on mousemove.
    $('#ptable').on('mousemove', '#pgrid', function(ev) {
        var pT = ev.pageY-$(this).offset().top;
        var pL = ev.pageX-$(this).offset().left;
        var mathx = pL-origin[0];
        var mathy = origin[1]-pT;
        $('#hover-x').text(parseInt(mathx));
        $('#hover-y').text(parseInt(mathy));
    });

    $('#help, #help-menu-wrapper').click(function() {
        $('#help-menu-wrapper').toggle();
    });

    $('#share').click(function() {
        if (points_empty()) return;

        // Create the point string.
        var pstring = '';
        for(var i=0; i < points.length; i+=1) {
            pstring += points[i].slice(1).toString();
            pstring += (i==points.length-1) ? "" : ","
        }
        pstring = '#'+encodeURIComponent(pstring);

        // Get the base url.
        var hi  = location.href.indexOf('#');
        var url = (hi == -1) ? location.href : location.href.slice(0, hi);

        url += pstring;

        $('body').append('<input id="share-url">')
        $('#share-url').val(url).css({
            top: $(this).offset().top,
            left: $(this).offset().left+$(this).outerWidth(true)+5
        }).select()
    });

    $('body').on('focusout', '#share-url', function() { $(this).remove(); });

    $('#download').click(function() {
        if (points_empty()) return;

        var dat = "" 
        for(var i=0; i < points.length; i+=1) {
            dat += points[i].slice(1).toString() + '\n';
        }

        window.open("data:text/plain;charset=utf-8,"+encodeURIComponent("# x,y,label\n" + dat));
    });

    $('#clear').click(function() {
        if (points_empty()) return;

        if (points.length != 0 && confirm("Are you sure?")) {
            pid = 0;
            points = Array();
            $('div.point').remove();
            location.hash = "";
        }
    });

});
