s.options.sampleRate_(24000).blockSize_(1024).hardwareBufferSize_(8192*4).memoryLocking_(true).memSize_(8192*4);
s.boot;

s.waitForBoot({
	Ndef(\foo, {SinOsc.ar(LFNoise0.kr(3!2).range(100, 1000))*0.2}).play;
});
