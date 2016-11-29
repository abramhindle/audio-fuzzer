<CsoundSynthesizer>
<CsOptions>
</CsOptions>
<CsInstruments>

sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1

instr 1 

ilen   filelen p4
print  ilen
ichn   filenchnls  p4
p3 = ilen*1.01

asig diskin2 p4, 1, 0, 0
aorig = asig

;;; reverb effect
asig, asigR freeverb asig, asig, 0.221771454719 , 0.908496106259 



     out    asig

endin
</CsInstruments>
<CsScore>

i 1 0 0.01 "testing.wav"

e
</CsScore>
</CsoundSynthesizer>