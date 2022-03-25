e = ();

// read env variables
e[\scName] = "SC_NAME".getenv;
e[\scPort] = "SC_PORT".getenv.asInteger;
e[\scPubilcIp] = "SUPERCOLLIDER_PUBLIC_IP".getenv;
e[\janusOutPort] = "JANUS_OUT_PORT".getenv.asInteger;
e[\janusInPort] = "JANUS_IN_PORT".getenv.asInteger;
e[\janusOutRoom] = "JANUS_OUT_ROOM".getenv.asInteger;
e[\janusInRoom] = "JANUS_IN_ROOM".getenv;
e[\janusPublicIp] = "JANUS_PUBLIC_IP".getenv;
e[\useInput] = ("SUPERCOLLIDER_USE_INPUT".getenv ? 0).asInteger;
e[\oscBackendHost] = "BACKEND_OSC_HOST".getenv;
e[\oscBackendPort] = "BACKEND_OSC_PORT".getenv.asInteger;

s = Server(e[\scName], NetAddr("127.0.0.1", e[\scPort]));
Server.default = s;

s.options.sampleRate_(48000).memoryLocking_(true).memSize_(8192*4);
s.options.numOutputBusChannels =2;
s.options.device = "default:%".format(e[\scName]);

"Booting server % on port %".format(e[\scName], e[\scPort]).postln;

s.boot;

s.waitForBoot({
	Ndef(\foo, {|out|
		var sig;
		var n = 16;

		sig = SinOsc.ar(
			freq: LFDNoise3.kr(0.02!n).exprange(10, LFDNoise1.kr(0.01).exprange(1000, 10000)) * ([0.0, 0.01].midiratio),
			phase: LocalIn.ar(n) * LFDNoise1.kr(0.1!n);
		) * LFDNoise3.kr(0.1!n).exprange(0.1, 1.0);
		sig = CombC.ar(
			sig,
			maxdelaytime: 0.2,
			delaytime: LFDNoise1.kr(0.05!n).range(0.01, 0.2),
			decaytime: (LFDNoise1.kr(0.1!n)),
		);
		LocalOut.ar(
			CombC.ar(
				in: sig,
				maxdelaytime: 0.2,
				delaytime: LFDNoise1.kr(0.1!n).range(0.01, 0.2),
				decaytime: LFDNoise0.kr(1.0!n)*10
			) * 0.5;
		);
		sig = Splay.ar(sig, LFDNoise1.kr(LFDNoise1.kr(1.0)*5));
		sig = sig * \amp.kr(0.9);
		Out.ar(out, sig.tanh);
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

OSCdef(\foo, {|msg|
	["received", msg].postln;
	Ndef(\foo).set(\freq, msg[1]);
}, path: "foo");

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
