e = ();

// read env variables
e[\scName] = "SC_NAME".getenv;
e[\scSynthPort] = "SC_SYNTH_PORT".getenv.asInteger;
e[\scLangPort] = NetAddr.langPort;
e[\scPubilcIp] = "SUPERCOLLIDER_PUBLIC_IP".getenv;
e[\janusOutPort] = "JANUS_OUT_PORT".getenv.asInteger;
e[\janusInPort] = "JANUS_IN_PORT".getenv.asInteger;
e[\janusOutRoom] = "JANUS_OUT_ROOM".getenv.asInteger;
e[\janusInRoom] = "JANUS_IN_ROOM".getenv;
e[\janusPublicIp] = "JANUS_PUBLIC_IP".getenv;
e[\useInput] = ("SUPERCOLLIDER_USE_INPUT".getenv ? 0).asInteger;
e[\oscBackendHost] = "BACKEND_OSC_HOST".getenv;
e[\oscBackendPort] = "BACKEND_OSC_PORT".getenv.asInteger;

s = Server(e[\scName], NetAddr("127.0.0.1", e[\scSynthPort]));
Server.default = s;

s.options.sampleRate_(48000).memoryLocking_(true).memSize_(8192*4);
s.options.numOutputBusChannels =2;
s.options.device = "default:%".format(e[\scName]);

"Booting server % on port %".format(e[\scName], e[\scSynthPort]).postln;

s.boot;

s.waitForBoot({
	Ndef(\gps, {
		var lon = \lon.kr(47.086395263672, lag: 4.0);
		var lat = \lat.kr(15.429121017456, lag: 4.0);
		var freq = \freq.kr(100.0);

		var extractor = {|i| 12.collect({|j| (i * (10**j)) % 10})};

		var lons = extractor.(lon);
		var lats = extractor.(lat);

		var sineSig = (1..11).collect({|i|
			SinOsc.ar(freq*(1+lons.wrapAt(i+3))) * EnvGen.kr(Env.perc(attackTime: lons.wrapAt(i+5)/5, releaseTime: lons.wrapAt(i+7)/5), gate: Impulse.kr(i/(5*lons[i])));
		});

		var sawSig = (1..11).collect({|i|
			var cSig = Saw.ar(freq*(1+lats.wrapAt(i+2))) * EnvGen.kr(Env.perc(attackTime: lats.wrapAt(i+5)/5, releaseTime: lats.wrapAt(i)/5), gate: Impulse.kr(i/(5*lats[i])));
			cSig = BPF.ar(cSig, freq*(1+lons.wrapAt(i+2)), rq: 0.2);
			cSig;
		});

		sineSig = Splay.ar(sineSig);
		sawSig = Splay.ar(sawSig);

		sineSig = sineSig + sawSig;

		sineSig;
	}).play;

	Ndef(\bar, {|out|
		var sig;
		sig = SoundIn.ar(0);
		sig = DelayL.ar(sig, maxdelaytime: 2.0, delaytime: 1.2*[1.0, 1.1]);
		sig = (sig*4) * SinOsc.ar(LFDNoise1.kr(2!2).exprange(100, 4000))*0.4;
		sig = (sig*4).tanh;
		Out.ar(out, sig);
	}).play;
});

OSCdef(\gps, {|msg|
	var parsed = ();
	msg[1..].pairsDo({|key, value| parsed[key.asSymbol] = value});
	parsed.postln;
	Ndef(\gps).set(\lon, parsed[\lon]);
	Ndef(\gps).set(\lat, parsed[\lat]);
}, path: "/gps");

OSCdef(\speak, {|msg|
	["speak", msg].postln;
	Tdef(\speak, {
		var buffer;
		buffer = Buffer.read(s, "/data" +/+ msg[1]);
		0.1.wait; //takes some time on the server to load the buffer?
		buffer.play;
	}).play;
}, path: "/speak");


Tdef(\live, {
	inf.do({
		// as SC does not have a nice way to create a JSON we simply send an
		// array in [key, value, key, value] format
		var message = e.keys.collect({|k| [k, e[k]]}).asArray.flatten;

		NetAddr(e[\oscBackendHost], e[\oscBackendPort]).sendMsg("/live", *message);
		5.0.wait;
	});
}).play;

OSCFunc.trace(true, true);
