GenCasterStatus {
	classvar <success;
	classvar <failure;
	classvar <ready;
	classvar <finished;
	classvar <beacon;
	classvar <received;

	*initClass {
		success = "SUCCESS";
		failure = "FAILURE";
		ready = "READY";
		finished = "FINISHED";
		beacon = "BEACON";
		received = "RECEIVED";
	}
}

GenCasterVerbosity {
	classvar <debug;
	classvar <info;
	classvar <warning;
	classvar <error;

	*initClass {
		debug = 10;
		info = 20;
		warning = 30;
		error = 40;
	}
}

GenCasterServer {
	var <name;
	var <synthPort;
	var <langPort;
	var <publicIP;

	var <janusOutPort;
	var <janusInPort;
	var <janusOutRoom;
	var <janusInRoom;
	var <janusPublicIP;

	var <useInput;

	var <oscBackendHost;
	var <oscBackendPort;


	var <>verbosity;

	// private
	var <>oscBackendClient;
	var <>environment; // shall this be a proxy space?
	var <>server;

	// basically a constructor which allows us to set
	// the necessary values directly or via env variables
	// as fallback - a "bit" verbose, but well
	*new {arg
		name = nil,
		synthPort = nil,
		langPort = nil,
		publicIP = nil,
		janusOutPort = nil,
		janusInPort = nil,
		janusOutRoom = nil,
		janusInRoom = nil,
		janusPublicIP = nil,
		useInput = nil,
		oscBackendHost = nil,
		oscBackendPort = nil,
		verbosity = nil;

		name = name ? "SC_NAME".getenv ? "GENCASTER_LOCAL";
		synthPort = synthPort ? ("SC_SYNTH_PORT".getenv ? 57110).asInteger;
		langPort = langPort ? NetAddr.langPort ? 57120;
		publicIP = publicIP ? "SUPERCOLLIDER_PUBLIC_IP".getenv;
		janusOutPort = janusOutPort ? ("JANUS_OUT_PORT".getenv ? 0).asInteger;
		janusInPort = janusInPort ? ("JANUS_IN_PORT".getenv ? 0).asInteger;
		janusOutRoom = janusOutRoom ? "JANUS_OUT_ROOM".getenv;
		janusInRoom = janusInRoom ? "JANUS_IN_ROOM".getenv;
		janusPublicIP = janusPublicIP ? "JANUS_PUBLIC_IP".getenv;
		useInput = useInput ? ("SUPERCOLLIDER_USE_INPUT".getenv ? 0).asInteger;
		oscBackendHost = oscBackendHost ? "BACKEND_OSC_HOST".getenv ? "127.0.0.1";
		oscBackendPort = oscBackendPort ? ("BACKEND_OSC_PORT".getenv ? 8082).asInteger;
		verbosity = verbosity ? ("SC_VERBOSITY".getenv ? GenCasterVerbosity.info).asInteger;

		^super.newCopyArgs(
			name,
			synthPort,
			langPort,
			publicIP,
			janusOutPort,
			janusInPort,
			janusOutRoom,
			janusInRoom,
			janusPublicIP,
			useInput,
			oscBackendHost,
			oscBackendPort,
			verbosity,
		).init;
	}

	init {
		oscBackendClient = NetAddr(
			hostname: oscBackendHost,
			port: oscBackendPort,
		);
		environment = this.serverInfo;
		environment[\oscBackendClient] = oscBackendClient;
		environment[\this] = this;
	}

	*arrayToEvent {

	}

	serverInfo {
		^(
			name: name,
			synthPort: synthPort,
			langPort: langPort,
			publicIP: publicIP,
			janusOutPort: janusOutPort,
			janusInPort: janusInPort,
			janusOutRoom: janusOutRoom,
			janusInRoom: janusInRoom,
			janusPublicIP: janusPublicIP,
			useInput: useInput,
			oscBackendHost: oscBackendHost,
			oscBackendPort: oscBackendPort,
		);
	}

	*eventToArray {|event|
		// as SC does not have a nice way to create a JSON we simply send an
		// array in [key, value, key, value] format
		var array = event.keys.collect({|key| [key, event[key]]}).asArray.flatten;
		^array;
	}

	sendAck {|status, uuid=nil, message=nil, address=nil|
		message = message ? ();
		message[\uuid] = uuid ? 0;
		message[\status] = status;
		address = address ? "/ack";

		if(verbosity<=GenCasterVerbosity.debug, {
			if(status==GenCasterStatus.beacon, {
				"BEACON".postln;
			}, {
				"%\t%\t%".format(status, message.uuid, message).postln;
			});
		});
		oscBackendClient.sendMsg(address, *GenCasterServer.eventToArray(message));

	}

	postServerInfo {
		"### GenCaster server ###".postln;
		this.serverInfo.pairsDo({|k, v|
			"%: %".format(k, v).postln;
		});
		"### /GenCaster server ###".postln;
	}

	startServer {
		server = Server(
			name: name,
			addr: NetAddr(hostname: "127.0.0.1", port: synthPort),
		);
		server.options.sampleRate_(48000).memoryLocking_(true).memSize_(8192*4);
		server.options.numOutputBusChannels =2;
		server.options.device = "default:%".format(name);
		server.options.bindAddress = "0.0.0.0";
		server.options.maxLogins = 2;
		Server.default = server;

		"Booting server % on port %".format(name, synthPort).postln;
		server.waitForBoot(onComplete: this.postStartServer);
	}

	beacon { |waitTime=5.0|
		^Tdef(\beacon, {
			inf.do({
				this.sendAck(
					status: GenCasterStatus.beacon,
					uuid: 0,
					message: this.serverInfo,
					address: "/beacon",
				);
				waitTime.wait;
			});
		});
	}

	instructionReceiver {
		^OSCdef(\instructionReceiver, {|msg, time, addr, recvPort|
			var uuid = msg[1];
			var function = (msg[2] ? "{}").asString;
			this.sendAck(status: GenCasterStatus.received, uuid: uuid);
			{
				var returnValue = function.interpret.(environment);
				this.sendAck(
					status: GenCasterStatus.finished,
					uuid: uuid,
					message: (returnValue: returnValue),
				);
			}.fork;
		}, path: "/instruction");
	}

	postStartServer {
		"Finished booting server".postln;
		this.beacon.play;
		this.instructionReceiver;
	}
}
