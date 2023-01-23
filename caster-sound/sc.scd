g = GenCasterServer(verbosity: GenCasterVerbosity.debug);

g.postServerInfo();

g.startServer();

// OSCFunc.trace(true, true);

s.waitForBoot({
    Ndef(\test, {
        var delay;
        var speed = 0.5;
        var pitches = [60, 67, 65, 69] + (g.synthPort%16);
        var trig = Impulse.kr(speed);
        var pitch = TChoose.kr(trig!pitches.size, pitches.collect({|i| i + LFDNoise3.kr(0.1).range(-0.2, 0.2)}));
        var sig = SyncSaw.ar(
            syncFreq: pitch.midicps * Select.kr(ToggleFF.kr(Impulse.kr(speed/7), [1.0, 0.5])),
            sawFreq: pitch.scramble.midicps * TChoose.kr(Dust.kr(0.2), [0.5, 1.0, 1.5]),
        );
        var envs = Saw.ar(TChoose.kr(Impulse.kr(speed/4), (1..8)/4) * pitch.midicps/[100, 200, 400, 300], LFDNoise1.kr(1.0!4).range(0.7, 1.2)).lag(LFDNoise1.kr(0.5).range(0.01, 0.5));
        sig = Splay.ar(sig*envs) * 0.2;
        sig = Splay.ar(LPF.ar(sig, LFDNoise3.kr(1.0!2).exprange(1000, 4000)));
        delay = Splay.ar(
            CombL.ar(
                in: sig,
                maxdelaytime: speed.reciprocal,
                delaytime: (1..10).scramble/(10/(speed.reciprocal)),
                decaytime: 15,
                mul: 0.5,
            )
        );
        sig + delay;
    }).play;

    Ndef(\micTest, {
        var sig = SoundIn.ar(0);
        FreqShift.ar(sig, 100);
    }).play;
});
