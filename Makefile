PLAYER=mplayer
EVERYTHING=audiofuzzer.py testing.wav audio-fuzzer.csd.jinja2
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

tree: tree-out.wav
	$(PLAYER) tree-out.wav

tree-out.wav: $(EVERYTHING)
	python audiofuzzer.py -i testing.wav -o tree-out.wav -effect tree

manytrees: manytrees-out.wav
	$(PLAYER) manytrees-out.wav


manytrees-out.wav: $(EVERYTHING)
	python audiofuzzer.py -i testing.wav -o manytrees-out.wav -effect manytrees


rand: rand-out.wav
	$(PLAYER) rand-out.wav

rand-out.wav: $(EVERYTHING)
	python audiofuzzer.py -i testing.wav -o rand-out.wav -effect rand

manyrand: manyrand-out.wav
	$(PLAYER) manyrand-out.wav


manyrand-out.wav: $(EVERYTHING)
	python audiofuzzer.py -i testing.wav -o manyrand-out.wav -effect manyrand

clean:
	rm subtlereverb-out.wav reverb-out.wav default-out.wav manytrees-out.wav tress-out.wav \
	rand-out.wav manyrand-out.wav || echo OK
