s.boot;

s.waitForBoot({
	Ndef(\foo, {SinOsc.ar(LFNoise0.kr(3!2).range(100, 1000))*0.2}).play;
	s.record("foo.wav");
	5.wait;
	s.stopRecording;
});
