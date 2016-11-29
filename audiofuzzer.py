import random
import jinja2 
import argparse
import os
import json

def get_random_generator(name):
    """ I generate functions that choose random numbers """
    if name == "uniform":
        def uniform(obj):
            return random.uniform(obj.min,obj.max)
        return uniform
    else:
        raise "I don't have a generator for %s" % name

class Param(object):
    """ I represent parameters and generator random values from them """
    def __init__(self,d):
        self.name = d["name"]
        self.v    = d.get("v",None)
        self.min  = d.get("min",0.0)
        self.max  = d.get("max",0.99)
        self.random = d.get("random","uniform")
        # I am a state pattern
        self.random_state = get_random_generator(self.random)
    
    def value(self):
        if self.v == None:
            return self.random_state(self)
        return self.v

class Effect(object):
    def __init__(self):
        """ effect base class """
        self.params = []

    def gen_params(self):
        out = dict()
        for param in self.params:
            name  = param.name
            value = param.value()
            out[name] = value
        return out

class Reverb(Effect):
    """ I represent Reverb """
    name = "Reverb"
    def __init__(self,d=None):
        if d == None:
            d = dict()
        self.name = Reverb.name
        self.roomsize = Param({"name":"roomsize",
               "v":d.get("roomsize",None),
               "min":d.get("roomsize_min",0.0),
               "max":d.get("roomsize_max",1.0)
        })
        self.damp = Param({"name":"damp",
               "v":d.get("damp",None),
               "min":d.get("damp_min",0.0),
               "max":d.get("damp_max",1.0)
        })
        self.params = [self.roomsize, self.damp]

class Tree(Effect):
    """ I represent a Tree """
    name = "Tree"
    def __init__(self,d=None):
        if d == None:
            d = dict()
        self.name = Tree.name
        self.q = Param({"name":"q",
               "v":d.get("q",None),
               "min":d.get("q_min",0.1),
               "max":d.get("q_max",2.0)
        })
        self.cf = Param({"name":"cf",
               "v":d.get("cf",None),
               "min":d.get("cf_min",400),
               "max":d.get("cf_max",4000)
        })
        self.params = [self.q, self.cf]

class Highpass(Effect):
    """ I represent a Tree """
    name = "highpass"
    def __init__(self,d=None):
        if d == None:
            d = dict()
        self.name = Highpass.name
        self.freq = Param({"name":"freq",
               "v":d.get("freq",None),
               "min":d.get("freq_min",60),
               "max":d.get("freq_max",1000)
        })
        self.params = [self.freq]


class WhiteNoise(Effect):
    """ I represent a Whitenoise """
    name = "whitenoise"
    def __init__(self,d=None):
        if d == None:
            d = dict()
        self.name = WhiteNoise.name
        self.amp = Param({"name":"amp",
               "v":d.get("amp",None),
               "min":d.get("amp_min",0),
               "max":d.get("amp_max",1.0)
        })
        self.beta = Param({"name":"beta",
                          "v":d.get("beta",None),
                          "min":d.get("beta_min",0),
                          "max":d.get("beta_max",1.0)
        })
        self.params = [self.amp, self.beta]

        

        
def gen_reverb(params):
    params["effect"]["reverb"] = Reverb().gen_params()

def gen_subtlereverb(params):    
    params["effect"]["reverb"] = Reverb({
        "roomsize_min":0.01,
        "roomsize_max":0.3,
        "damp_min":0.9,
        "damp_max":0.99
    }).gen_params()

def gen_tree(params):
    params["effect"]["tree"] = Tree().gen_params()

def gen_manytrees(params):
    params["effect"]["tree"] = Tree({
        "cf_min":400.0,
        "cf_max":1000.0
    }).gen_params()

def gen_highpass(params):
    params["effect"]["highpass"] = Highpass({}).gen_params()

def gen_highhighpass(params):
    params["effect"]["highpass"] = Highpass({
        "freq_min":800.0,
        "freq_max":2000.0
    }).gen_params()

def gen_whitenoise(params):
    params["effect"]["whitenoise"] = WhiteNoise({}).gen_params()

def gen_hiss(params):
    params["effect"]["whitenoise"] = WhiteNoise({
        "amp_min":0.01,
        "amp_max":0.1,
        "beta_min":0.5,
        "beta_max":1.0
    }).gen_params()


    
def gen_1khighpass(params):
    params["effect"]["highpass"] = Highpass({
        "freq":1000.0
    }).gen_params()
    
def gen_none(params):
    """DO Nothing"""

def gen_rand(params):
    f = random.sample(effects.values(),1)[0]
    print f
    f(params)

def gen_manyrand(params):
    for i in range(0,random.randrange(2,6)):
        gen_rand(params)
    
# sign up effects
effects = {
    "reverb":gen_reverb,
    "subtlereverb":gen_subtlereverb,
    "manytrees":gen_manytrees,
    "tree":gen_tree,
    "rand":gen_rand,
    "manyrand":gen_manyrand,
    "highpass":gen_highpass,
    "highhighpass":gen_highhighpass,
    "1khighpass":gen_1khighpass,
    "whitenoise":gen_whitenoise,
    "hiss":gen_hiss,
    "none":gen_none
}
# so we can provide help!
effect_list_str = ", ".join(effects.keys())

parser = argparse.ArgumentParser(description='Audio Fuzzer')
parser.add_argument('-i', default="in.wav", help='Input wavefile')
parser.add_argument('-o', default="out.wav", help="Output wavefile")
parser.add_argument('-csd', default="audio-fuzzer.csd", help="Output CSD file")
parser.add_argument('-stereo', action="store_true", help="Output stereo wav files")
parser.add_argument('-effect', default="none", nargs='*', help="Which effect to choose from: %s" % effect_list_str)

args = parser.parse_args()

# get the jinja going
env = jinja2.Environment(autoescape=False,
                  loader=jinja2.FileSystemLoader('./'))    
template = env.get_template("audio-fuzzer.csd.jinja2")

# init our data to template
params = {
    "wavefile":args.i,    
    "effect":{},
    "stereo":int(args.stereo)
}

fd = open("params.json","w")
fd.write(json.dumps(params))
fd.close()


# apply effects
for effect in args.effect:
    effects[effect](params)

# write out template out
fd = open(args.csd,"w")
out = template.render(params)
fd.write(out)
print out
fd.close()

# get csound to render it
command = "csound %s -o %s -W" % (args.csd,args.o)
os.system(command)
