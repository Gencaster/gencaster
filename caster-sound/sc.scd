s.options.sampleRate_(48000).memoryLocking_(true).memSize_(8192*4);
s.boot;

s.waitForBoot({
	Ndef(\foo, {|out|
		var sig;
		sig = SinOsc.ar([LFNoise0.kr(3.0).range(100, 1000), \freq.kr(200.0)])*0.2;
		Out.ar(out, sig);
	}).play;
});

OSCdef(\foo, {|msg|
	["received", msg].postln;
	Ndef(\foo).set(\freq, msg[1]);
}, path: "foo");
