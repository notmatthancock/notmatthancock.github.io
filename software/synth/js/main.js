$(function() {
    function makeDistortionCurve(amount) {
        if ( amount == 0 ) return null;
        var n_samples = 44100;
        var curve = new Float32Array(n_samples);
        var delta = 2/(n_samples-1);
        for (var i=0; i<n_samples; i++) curve[i] = 0.8 * Math.tanh(amount*(-1+delta*i)) / Math.tanh(amount);
        return curve;
    };

	synth = function( context ) {
		this.context = context;
		this.num_oscs = 3;
		this.depressed_notes = [];

		// initialize oscillators
		this.osc = [];
		for ( i=1; i<=this.num_oscs; i += 1 ) {
			this.osc[i] = {
				oct: 4,
				type: (i==1) ? 'triangle' : ( (i==2) ? 'sawtooth' : 'square' ),
				route: (i==1)?1:0
			};
			
			// mono oscillators
			this.osc[i].mono = context.createOscillator(); this.osc[i].mono.type = this.osc[i].type;
			this.osc[i].amp = context.createGain(); this.osc[i].mono.connect( this.osc[i].amp );
			this.osc[i].amp.gain.setValueAtTime( 0, this.context.currentTime );
			this.osc[i].mono.start( this.context.currentTime );
		}
		
		// polyphony
		this.poly = true;
		// portamento
		this.slide = 0.0;
		
		// amp envelope
		this.amp_env = {
			attack: 0.03,
			decay: 0.5,
			release: 0.2
		};
		
		// filt envelope
		this.filt_env = {
			attack: 0.1,
			attack_percent: 0.333,
			decay: 0.1,
			decay_percent: 0.333,
			release: 0.1,
			amt_1: 0,
			amt_2: 0
		};
		this.filt_min = 10;
		this.filt_max = 20000;
		
		// filters
		this.filt1 = this.context.createBiquadFilter();
		this.filt1.frequency.value = 10000; this.filt1.Q.value = 1;
		this.filt2 = this.context.createBiquadFilter();
		this.filt2.frequency.value = 10000; this.filt2.Q.value = 1;
		
		// reverb
		this.reverb_dry = 1.0;
		this.reverb_wet = 0.0;
		var request = new XMLHttpRequest();
        request.responseType = "arraybuffer";
		request.open("GET", "./ir.mp3", true);
        
        this.reverb = this.context.createConvolver();

        var this_ = this;
        request.onload = function() {
            var audioData = request.response;
            this_.context.decodeAudioData( audioData, function(buffer) {
               buffer_ = buffer;
               soundSource = this_.context.createBufferSource();
               soundSource.buffer = buffer_;
               this_.reverb.buffer = buffer_;
            }, function(e) {"Error in handling audio data"+e.err});
        }
		
        request.send()

		this.dry = this.context.createGain(); this.dry.gain.value = 1.0;
		this.wet = this.context.createGain(); this.wet.gain.value = 0.0;
		
        // distortion
        this.distortion = this.context.createWaveShaper();
        this.distortion.curve = makeDistortionCurve(0.0);
        //this.distortion.oversample = '4x';

		// spectrum analyser
		this.spectrum = this.context.createAnalyser();
        this.spectrum.minDecibels = -90;
        this.spectrum.maxDecibels = -10;
        this.spectrum.fftSize = 32;
		
		// master volume
		this.master_gain = this.context.createGain();
		
		// connections
		this.osc[1].amp.connect( this.filt1 );
		this.filt1.connect( this.dry ); this.filt1.connect( this.reverb );
		this.filt2.connect( this.dry ); this.filt2.connect( this.reverb );
		this.reverb.connect( this.wet );
		this.dry.connect( this.distortion ); this.wet.connect( this.distortion );
        this.distortion.connect( this.master_gain );
		this.master_gain.connect( this.spectrum ); this.spectrum.connect( context.destination );
	}
	
	synth.prototype.playNote = function( freq ) {
		var now = this.context.currentTime;
		for ( var i=1; i <= this.num_oscs; i+=1 ) {
			if ( ! this.osc[i].route ) continue;
		
			if ( this.poly ) {
				// create oscillator
				var o = this.context.createOscillator();
				o.frequency.value = freq * Math.pow( 2, this.osc[i].oct-4 );
				o.type = this.osc[i].type; o.detune.value = this.osc[i].mono.detune.value;
				o.start( now );

				// create envelope node and connect
				var g = this.context.createGain();
				o.connect( g ); g.connect( this[ 'filt'+this.osc[i].route ] );

				// enveloping
				g.gain.setValueAtTime( 0, now );
				g.gain.linearRampToValueAtTime( 1, now + this.amp_env.attack );
				g.gain.linearRampToValueAtTime( this.amp_env.decay, now + this.amp_env.attack + this.amp_env.decay );
			
                synth.depressed_notes.push( [ o, g, i ] );
			} // end poly case
			else { // mono case
				this.osc[i].mono.frequency.linearRampToValueAtTime( freq * Math.pow( 2, this.osc[i].oct-4 ), now + this.slide );
				
				if ( ! this.depressed_notes.length ) {
					this.osc[i].amp.gain.cancelScheduledValues( now );
					this.osc[i].amp.gain.setValueAtTime(0,now);
					this.osc[i].amp.gain.linearRampToValueAtTime( 1, now + this.amp_env.attack );
					this.osc[i].amp.gain.linearRampToValueAtTime( this.amp_env.decay, now + this.amp_env.attack + this.amp_env.decay );
				}
				
                synth.depressed_notes.push( [ false, i, freq ] );
			} // end mono case
			
			if ( false ) {
			// filter env
			current_freq = this.filt1.frequency.value;
			sign = (this.filt_env.amt_1 < 0) ? -1 : 1;
			dist = this.filt_env.amt_1*((sign < 0) ? (current_freq-this.filt_min) : (this.filt_max-current_freq));
			mod_freq = current_freq + dist;
			attack_freq = mod_freq - dist*this.filt_env.attack_percent;
			decay_freq = mod_freq - dist*(this.filt_env.decay_percent + this.filt_env.attack_percent);
		
			this.filt1.frequency.cancelScheduledValues( now );
			this.filt1.frequency.setValueAtTime(mod_freq,now);
			this.filt1.frequency.linearRampToValueAtTime( attack_freq, now + this.filt_env.attack );
			this.filt1.frequency.linearRampToValueAtTime( decay_freq, now + this.filt_env.attack + this.filt_env.decay + this.filt_env.release );
			this.filt1.frequency.linearRampToValueAtTime( current_freq, now + this.filt_env.attack + this.filt_env.decay + this.filt_env.release );
			}
		}
	}
	
	synth.prototype.releaseNote = function( freq ) {
		var now = this.context.currentTime; var indices = [];
		
		for ( var i=0; i < this.depressed_notes.length; i+=1 ) {
			var note = this.depressed_notes[i];
			if ( note[0] ) { // poly
				var f = freq*Math.pow( 2, this.osc[ note[2] ].oct - 4 );
				if ( parseInt( f ) == parseInt( note[0].frequency.value ) ) {
					// release envelope
					note[1].gain.cancelScheduledValues( now );
					note[1].gain.setValueAtTime( note[1].gain.value, now );
					note[1].gain.linearRampToValueAtTime( 0, now + this.amp_env.release );
	
					// kill note after envelopes are done
					note[0].stop( now + this.amp_env.release );
					delete note[1]; delete note[2];
				
					// add index to be removed
					indices.push( i );
				}
			}
			else { // mono
				if ( parseInt( freq*Math.pow( 2, this.osc[ note[1] ].oct - 4 ) ) == parseInt( note[2] ) ) indices.push( i );
			}
		}
		
		var tmp = [];
		
		for ( var i = 0; i < this.depressed_notes.length; i += 1 ) {
			if ( indices.indexOf(i) == -1 ) tmp.push( this.depressed_notes[i] );
		}
		
		this.depressed_notes = tmp;
		
		if ( ! this.poly ) {
			if ( this.depressed_notes.length ) {
				for ( var i=1; i <= this.num_oscs; i+=1 ) {
					this.osc[i].mono.frequency.setValueAtTime( this.depressed_notes[ this.depressed_notes.length-1 ][2], now );
				}
			}
			else {
				for ( var i=1; i <= this.num_oscs; i+=1 ) {
					// release envelope
					this.osc[i].amp.gain.cancelScheduledValues( now );
					this.osc[i].amp.gain.setValueAtTime( this.osc[i].amp.gain.value, now );
					this.osc[i].amp.gain.linearRampToValueAtTime( 0, now + this.amp_env.release );
				}
			}
		}
	}; // end releaseNote

	// dom:
    // waveshape changes
    $(document).on('click.seq', '.osc .shape', function() {
        var num = parseInt( $(this).attr('num') );
        
        if ( $(this).hasClass('sawtooth') ) {
            $(this).toggleClass('sawtooth triangle');
            window.synth.osc[num].type = window.synth.osc[num].mono.type = 'triangle';
        }
        else if ( $(this).hasClass('triangle') ) {
            $(this).toggleClass('triangle square');
            window.synth.osc[num].type = window.synth.osc[num].mono.type = 'square';
        }
        else if ( $(this).hasClass('square') ) {
            $(this).toggleClass('square sine');
            window.synth.osc[num].type = window.synth.osc[num].mono.type = 'sine';
        }
        else if ( $(this).hasClass('sine') ) {
            $(this).toggleClass('sine sawtooth');
            window.synth.osc[num].type = window.synth.osc[num].mono.type = 'sawtooth';
        }
        
        window.synth.depressed_notes.forEach( function(note) {
            if ( note[2] == num ) {
                note[0].type = window.synth.osc[num].type;
            }
        });
    });
    
    $(document).on('input change', '.osc-oct', function() {
        $('#'+this.id+'-disp').val( $(this).val() );
        var num = parseInt( $(this).attr('num') );
        var oct = parseInt( $(this).val() );
        var mul = Math.pow( 2, oct - window.synth.osc[num].oct );
        window.synth.osc[num].oct = oct;
        window.synth.depressed_notes.forEach( function(note) {
            if ( note[2]==num ) {
                note[0].frequency.setValueAtTime( note[0].frequency.value * mul, window.synth.context.currentTime );
            }
        });
    });
    
    $(document).on('input change', '.osc-detu', function() {
        var val = parseFloat( $(this).val() );
        $('#'+this.id+'-disp').val( val );
        var num = parseInt( $(this).attr('num') );
        window.synth.osc[num].mono.detune.value = val;
        window.synth.depressed_notes.forEach( function(note) {
            if ( note[2] == num ) {
                note[0].detune.value = val;
            }
        });
    });
    
    $(document).on('input change', '.osc-route input', function() {
        var to = parseInt( $(this).attr('to') );
        var num =  parseInt( $(this).attr('num') );
        window.synth.osc[ num ].route = to;
        if ( to == 0 ) {
            $('#filt-1-route-indicators td#'+num).removeClass('on').addClass('off');
            $('#filt-2-route-indicators td#'+num).removeClass('on').addClass('off');
            window.synth.osc[num].amp.disconnect();
        }
        else if ( to == 1 ) {
            $('#filt-1-route-indicators td#'+num).addClass('on').removeClass('off');
            $('#filt-2-route-indicators td#'+num).addClass('off').removeClass('on');
            window.synth.osc[num].amp.disconnect();
            window.synth.osc[num].amp.connect( window.synth.filt1 );
        }
        else if ( to == 2 ) {
            $('#filt-2-route-indicators td#'+num).addClass('on').removeClass('off');
            $('#filt-1-route-indicators td#'+num).addClass('off').removeClass('on');
            window.synth.osc[num].amp.disconnect();
            window.synth.osc[num].amp.connect( window.synth.filt2 );
        }
    });
    
    $(document).on('input change', '#amp-envelopes input', function() {
        var val = parseFloat( $(this).val() );
        window.synth.amp_env[ this.id ] = val;
        if ( this.id == 'release' ) {
            $('#slide').attr('max', val);
            if ( synth.slide > val ) synth.slide = val;
        }
    });
    
    $(document).on('input change', '#filt-envelopes input', function() {
        var val = parseFloat( $(this).val() );
        window.synth.filt_env[ this.id ] = val;
    });
    
    $(document).on('input change', '#master-gain', function() {
        window.synth.master_gain.gain.value = parseFloat($(this).val())
    });
    
    $(document).on('input change', '#master-reverb', function() {
        window.synth.dry.gain.value = 1.0 - parseFloat($(this).val());
        window.synth.wet.gain.value = parseFloat($(this).val());
    });
    
    $(document).on('input change', '#distortion', function() {
        window.synth.distortion.curve = makeDistortionCurve( parseFloat($(this).val()) );
    });
    
    $(document).on('input change', '.freq', function() {
        window.synth['filt'+$(this).attr('num')].frequency.setValueAtTime( parseFloat($(this).val()), audio_context.currentTime );
    });
    
    $(document).on('input change', '.reso', function() {
        window.synth['filt'+$(this).attr('num')].Q.setValueAtTime( parseFloat($(this).val()), audio_context.currentTime );
    });
    
    $(document).on('input change', '.freq-type', function() {
        window.synth['filt'+$(this).attr('num')].type = $(this).val();
    });
    
    $(document).on('input change', '.poly', function() {
        window.synth.poly = (this.id == 'poly');
    });
    
    $(document).on('input change', '#slide', function() {
        window.synth.slide = parseFloat( $(this).val() );
    });
    
    $(document).on('click.seq', 'td.white,td.black', function() {
        window.synth.playNote( $(this).parent().attr('freq') );
    });
    
    $(document).on('input change', '.modf', function() {
        window.synth.filt_env['amt_'+$(this).attr('num')] = parseFloat( $(this).val() );
    });
    
    $(document).on('click.seq', '#kill', function() {
        window.synth.depressed_notes.forEach( function(note) {
            note[0].stop(window.synth.context.currentTime); delete note[1]; delete note[2];
        });
        window.synth.depressed_notes = [];
        for ( var i=1; i <= 3; i+=1 ) window.synth.osc[i].amp.gain.setValueAtTime( 0, window.synth.context.currentTime );
    });
    
    // initialization stuff
    try {
        window.AudioContext = window.AudioContext||window.webkitAudioContext;
        audio_context = new AudioContext();
    }
    catch(e) {
        $('#content').html('<div style="text-align:center; font-size: 24px;">Web Audio API is not supported in this browser :(</div>')
    }
    
    window.synth = new synth( audio_context );

	keyboard = qwertyHancock({
		id: "keyboard",
		width: $('#synth').width(),
		hoverColour: '#efeb92'
	});
	
	keyboard.keyDown( function( note, freq ) {
		synth.playNote( freq );
	});
	
	keyboard.keyUp( function( note, freq ) {
		synth.releaseNote( freq );
	});
	
    rand_color = function() {
        return "rgb("+parseInt(Math.random()*255)+","+parseInt(Math.random()*255)+","+parseInt(Math.random()*255)+")";
    }

	// spectrum
    $('#audio_spectrum_canvas').attr('width', $('#audio_spectrum_canvas').parent().width() );
    $('#audio_spectrum_canvas').attr('height', $('#audio_spectrum_canvas').parent().height() );
	var apc = $('#audio_spectrum_canvas')[0].getContext('2d');
    var apc_width = $('#audio_spectrum_canvas').width();
    var apc_height = $('#audio_spectrum_canvas').height();
    var buffer_length = synth.spectrum.frequencyBinCount;
    console.log(buffer_length);
    var barWidth = apc_width / buffer_length;
    var freqDomain = new Uint8Array(buffer_length);
	var timeDomain = new Uint8Array(buffer_length);
    apc.fillStyle = '#000000';

    update_spectrum = function() {
		synth.spectrum.getByteFrequencyData(freqDomain);
		synth.spectrum.getByteTimeDomainData(timeDomain);
		
		apc.clearRect(0, 0, apc_width, apc_height);

        var barHeight;
        var x = 0;

		for (var i = 0; i < buffer_length; i++) {
            barHeight = freqDomain[i] / 255.0 * apc_height;
            apc.fillRect(x, apc_height-barHeight, barWidth, barHeight);

            //var value_t = timeDomain[i];
            //var percent_t = value_t / 256;
            //var height_t = apc_height * percent_t;
            //var offset_t = apc_height - height_t - 1;
            //apc.fillRect(i * barWidth, offset_t, 1, 1);
            x += barWidth;
		}
        
        window.requestAnimationFrame( update_spectrum );
    };

    window.requestAnimationFrame( update_spectrum )

});
