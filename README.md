audio-fuzzer
============

Used to add effects to audio in a controlled or random manner.

Effects
=======

* reverb -- random reverb added to the signal
* subtlereverb -- a more subtle reverb added to the signal
* manytrees -- a lowpass filter meant to emulate trees dampening sound
* tree -- a small lowpass filter
* rand -- randomly choose 1 of these effects
* manyrand -- randomly choose 2 to 5 of these effects
* highpass -- a generic highpass randomly chosen
* highhighpass -- a highpass between 800hz and 2000hz
* 1khighpass -- a highpass at 1k
* none -- nothing

Dependencies
============

* csound - apt-get install csound
* jinja2 - pip install --user jinja2

Example install
===============

On Ubuntu or Debian:

```
    git clone https://github.com/abramhindle/audio-fuzzer.git
    cd audio-fuzzer
    pip install --user jinja2
    sudo apt-get install csound
```

Example use
===========

```
audio-fuzzer$ python audiofuzzer.py --help
usage: audiofuzzer.py [-h] [-i I] [-o O] [-csd CSD] [-stereo]
                      [-effect [EFFECT [EFFECT ...]]]

Audio Fuzzer

optional arguments:
  -h, --help            show this help message and exit
  -i I                  Input wavefile
  -o O                  Output wavefile
  -csd CSD              Output CSD file
  -stereo               Output stereo wav files
  -effect [EFFECT [EFFECT ...]]
                        Which effect to choose from: rand, highpass, manyrand,
                        manytrees, none, 1khighpass, tree, subtlereverb, hiss,
                        whitenoise, reverb, highhighpass


```

Fuzz up 1 file

```
    python  auduiofuzzer.py -i input.wav -o output.wav
```

Fuzz up 1 file and produce a stereo output

```
    python  auduiofuzzer.py -stereo -i input.wav -o output.wav
```

Add hiss

```
    python  auduiofuzzer.py -stereo -i input.wav -o output.wav -effect hiss
```
