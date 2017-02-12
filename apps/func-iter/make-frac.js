// Conversion code can be found on wikipedia
hsv_to_rgb = function(h,s,v) {
    var c  = s*v;
    var hp = h / 60.0;
    var x  = c*(1-Math.abs((hp % 2) - 1));

    if ( hp >= 0 && hp < 1 )
        var tmp = [c,x,0];
    else if ( hp >= 1 && hp < 2 )
        var tmp = [x,c,0];
    else if ( hp >= 2 && hp < 3 )
        var tmp = [0,c,x];
    else if ( hp >= 3 && hp < 4 )
        var tmp = [0,x,c];
    else if ( hp >= 4 && hp < 5 )
        var tmp = [x,0,c];
    else if ( hp >= 5 && hp <= 6 )
        var tmp = [c,0,x];

    var m = v-c;

    return [parseInt((tmp[0]+m)*255),parseInt((tmp[1]+m)*255), parseInt((tmp[2]+m)*255)];
}


generate_themed_color_scheme = function(colors,n) {
    // colors is an array of floats in [0,360]
    //
    // returns an array of length n where each element
    // is an random rgb color from colors with a random
    // variation on its hue and lightness.
    
    color_scheme = new Array(n);
    for(var i=0; i<n; i+=1) {
        var h = colors[ Math.floor(Math.random()*colors.length) ];
        var s = Math.random(); var v = Math.random()*0.9+0.1
//        if ( i==n-1)
            color_scheme[i] = hsv_to_rgb(h,s,v);
//        else
//            color_scheme[i] = [255, 255, 255];
    }
    return color_scheme;
}
generate_rand_color_scheme = function(n) {
	color_scheme = new Array(n);
	for (var i=0; i < n; i += 1) {
		color_scheme[i] = new Array(3);
        for (var j=0; j < 3; j+=1)
            color_scheme[i][j] = Math.floor( Math.random()*255 )
	}

	return color_scheme;
}

self.onmessage = function(msg) {
	var frac = JSON.parse( msg.data );
	frac.f = eval( frac.f );

    // generate_rand_color_scheme( frac.con_limit );
    var colors = generate_themed_color_scheme(frac.hues, frac.con_limit );
    var img_data = new Uint8ClampedArray(4*frac.width*frac.height);

    for( var i=0; i < frac.width; i+=1 ) {
        for( var j=0; j < frac.height; j+=1 ) {
            var ip = i*frac.height + j
            if ( !frac.color_only ) {
                // This is the point to be iterated.
                var p = [ frac.xMin + j*frac.xStep, frac.yMax - i*frac.yStep ];
                
                // While the norm of the current iterate is less than
                // the divergence limit, keep iterating.
                var k = 0;
                while ( Math.sqrt(p[0]*p[0] + p[1]*p[1]) < frac.div_limit ) {
                    p = frac.f( p ); k += 1;
                    if ( k >= frac.con_limit ) break;
                }
            
                frac.points[ip] = k;
            }

            for (var l=0; l<3; l+=1)
                 // we have to offset by 1 because every point survices at least one iteration
                img_data[4*ip+l] = colors[frac.points[ip]-1][l];
            // this is the alpha value for rgba
            img_data[4*ip+3] = 255
        }
        if ( !frac.color_only ) self.postMessage({topic: 'testing', iter: i});
    }
    
    // Send back the frac object
    if ( frac.color_only ) frac.color_only = false;
    self.postMessage({topic: 'frac', frac: JSON.stringify(frac)});

    // Finally we send back the image data
    self.postMessage({topic: 'image_data', image_data: img_data})

}//, false );
