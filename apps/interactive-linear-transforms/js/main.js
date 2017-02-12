$('td.bracket').css('font-size', $('td.bracket:first').parent().height()+10)
canb = document.getElementById('transformation-background');
ctxb = canb.getContext('2d');

//// Draw canvas axes background

// y-axis
ctxb.beginPath();
ctxb.moveTo(200, 0);
ctxb.lineTo(200, 400);
ctxb.stroke()

// upper point
ctxb.beginPath(); ctxb.moveTo(200, 0); ctxb.lineTo(195, 5); ctxb.stroke()
ctxb.beginPath(); ctxb.moveTo(200, 0); ctxb.lineTo(205, 5); ctxb.stroke()
ctxb.beginPath(); ctxb.moveTo(200, 400); ctxb.lineTo(195, 395); ctxb.stroke()
ctxb.beginPath(); ctxb.moveTo(200, 400); ctxb.lineTo(205, 395); ctxb.stroke()

ticks = [50, 100, 150, 250, 300, 350];
for (var i in ticks) {
    ctxb.beginPath(); ctxb.moveTo(195,ticks[i]); ctxb.lineTo(205,ticks[i]); ctxb.stroke();
}

// x-axis
ctxb.beginPath();
ctxb.moveTo(0, 200);
ctxb.lineTo(400, 200);
ctxb.stroke()

// upper point
ctxb.beginPath(); ctxb.moveTo(0, 200); ctxb.lineTo(5, 195); ctxb.stroke()
ctxb.beginPath(); ctxb.moveTo(0, 200); ctxb.lineTo(5, 205); ctxb.stroke()
ctxb.beginPath(); ctxb.moveTo(400, 200); ctxb.lineTo(395, 195); ctxb.stroke()
ctxb.beginPath(); ctxb.moveTo(400, 200); ctxb.lineTo(395, 205); ctxb.stroke()

ticks = [50, 100, 150, 250, 300, 350];
for (var i in ticks) {
    ctxb.beginPath(); ctxb.moveTo(ticks[i], 195); ctxb.lineTo(ticks[i], 205); ctxb.stroke();
}

//// end background

canf = document.getElementById('transformation-foreground');
ctxf = canf.getContext('2d');
ctxf.lineWidth = 2;

x = [50,100];
a = [[1.00,1.00],[1.00,-1.00]];
$('.matrix-value').each(function() {
    $(this).val( a[this.id[1]][this.id[2]].toFixed(2) )
});
y = [50,50];

md = false;
l = $(canf).offset().left;
t  = $(canf).offset().top;

drawVectors = function(pageX, pageY) {
    ctxf.clearRect(0,0,400,400);
    // defaults
    if (typeof(pageX)=='undefined') pageX = x[0]+l+200;
    if (typeof(pageY)=='undefined') pageY = 200-x[1]+t;
    
    x[0] = pageX - l - 200;
    x[1] = 200 - (pageY - t);

    // display x
    $('#x0').val( (x[0]/100).toFixed(2) ); $('#x1').val( (x[1]/100).toFixed(2) );
    // multiply
    y = [ a[0][0]*x[0] + a[0][1]*x[1], a[1][0]*x[0] + a[1][1]*x[1] ];
    // display y
    $('#y0').val( (y[0]/100).toFixed(2) ); $('#y1').val( (y[1]/100).toFixed(2) );

    // draw the x and y vectors, converting back to canvas coords...
    ctxf.beginPath();
    ctxf.moveTo(200,200);
    ctxf.lineTo(x[0]+200, 200-x[1]);
    ctxf.stroke();
    
    ctxf.beginPath();
    ctxf.arc(x[0]+200, 200-x[1], 4, 0, 6.2831853, false);
    ctxf.fillStyle = 'blue';
    ctxf.fill()
    ctxf.stroke();

    ctxf.beginPath();
    ctxf.moveTo(200,200);
    ctxf.lineTo(y[0]+200, 200-y[1]);
    ctxf.stroke();

    ctxf.beginPath();
    ctxf.arc(y[0]+200, 200-y[1], 4, 0, 6.2831853, false);
    ctxf.fillStyle = 'red';
    ctxf.fill()
    ctxf.stroke();
}

// init
drawVectors();

$(canf).on('mousedown', function(e) { md = true; drawVectors(e.pageX,e.pageY); });
$(canf).on('mouseup',   function() { md = false; });
$(canf).on('mousemove', function(e) { if (!md) return; drawVectors(e.pageX,e.pageY); });
$('input.matrix-value').on('change', function() {
    if ( ! isNaN($(this).val()) )
        a[this.id[1]][this.id[2]] = parseFloat(($(this).val())).toFixed(2);
    $(this).val( a[this.id[1]][this.id[2]] );
    drawVectors();
});
