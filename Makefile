PLAYER=mplayer

default-out.wav: audiofuzzer.py testing.wav audio-fuzzer.csd.jinja2
	python audiofuzzer.py -i testing.wav -o default-out.wav

default: default-out.wav
	$(PLAYER) default-out.wav

reverb: reverb-out.wav
	$(PLAYER) reverb-out.wav

reverb-out.wav: audiofuzzer.py testing.wav audio-fuzzer.csd.jinja2
	python audiofuzzer.py -i testing.wav -o reverb-out.wav -effect reverb

subtlereverb: subtlereverb-out.wav
	$(PLAYER) subtlereverb-out.wav

subtlereverb-out.wav: audiofuzzer.py testing.wav audio-fuzzer.csd.jinja2
	python audiofuzzer.py -i testing.wav -o subtlereverb-out.wav -effect subtlereverb

clean:
	rm subtlereverb-out.wav reverb-out.wav default-out.wav || echo OK
