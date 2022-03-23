q = q ? ();

q[\scName] = "SC_NAME".getenv;
q[\scPort] = "SC_PORT".getenv.asInteger;

s = Server(q[\scName], NetAddr("127.0.0.1", q[\scPort]));
Server.default = s;

s.options.sampleRate_(48000).memoryLocking_(true).memSize_(8192*4);
s.options.numOutputBusChannels =2;
s.options.device = "default:%".format(q[\scName]);

"Booting server % on port %".format(q[\scName], q[\scPort]).postln;

s.boot;

s.waitForBoot({
	Ndef(\foo, {|out|
		var sig;
		sig = SinOsc.ar([LFNoise0.kr(3.0).range(100, 1000), \freq.kr(rrand(100, 400))])*0.05;
		Out.ar(out, sig);
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
	var oscBackendHost = "BACKEND_OSC_HOST".getenv;
	var oscBackendPort = "BACKEND_OSC_PORT".getenv.asInteger;

	inf.do({
		NetAddr(oscBackendHost, oscBackendPort).sendMsg("/live", 1);
		5.0.wait;
	});
}).play;
