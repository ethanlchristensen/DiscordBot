audio_filters = {
    "sigma": "aresample=48000, asetrate=48000*0.8,bass=g=13:f=110:w=0.6",
    "nightcore": "aresample=48000, asetrate=48000*1.25",
    "pulsar": "apulsator=amount=1:width=2",
    "earrape": "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1",
    "bassboost": "bass=g=10",
    "nuclear": "apsyclip=level_in=64:level_out=64:clip=1",
    "softclip": "asoftclip=hard:output=1",
}
