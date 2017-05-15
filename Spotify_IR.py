#!/usr/bin/env python

from spotipy import Spotify
from nltk import sent_tokenize
from nltk.tokenize import WhitespaceTokenizer
import sys
import getopt

class Spotify_IR(object):
    def __init__(self):
        self.sp = Spotify()

    def name_shuffle(self, fname):
        '''
        Shuffle the fname into small pieces with nltk dependency parser
        :param fname: type: string; to input full query, e.g. "If I can't let it go out of my mind"
        :return: res as a string list, which includes all
        '''
        # Methogology to shuffle: Both computational/space complexity are O(n),
        # <1>. sentence split;
        # <2>. construct and return a list including all valid 3/4/5-grams without duplicates
        sents = sent_tokenize(fname)
        apptime_thres = 100 # using 1/2/3/4/5-grams appeared >= apptime_thres times.
        # Assuming googlebooks hashmap is available as GB_map, below used a mock GB_map ...
        GB_map = {
            (u'if',):3000,
            (u'if', u'i',):2000,
            (u'if', u'i', u'ca',):1000,
            (u'if', u'i', u'can\'t',):120,
            (u'let',):800,
            (u'let', u'it',):500,
            (u'let', u'it', u'go',):200,
            (u'let', u'it', u'go', u'out',):10,
            (u'out',):1000,
            (u'out', u'of',):800,
            (u'out', u'of', u'my',):300,
            (u'out', u'of', u'my', u'mind',):150,
            (u'i',):1000,
            (u'ca',):1000,
            (u'n\'t',):1000,
            (u'it',):1000,
            (u'go',):1000,
            (u'of',):1000,
            (u'my',):1000,
            (u'mind',): 1000,
        }
        res = []
        for s in sents:
            t = WhitespaceTokenizer().tokenize(s.lower())
            cur = 0
            while cur < len(t):
                tl = 0 # len of current n-gram
                while (tl <= 4) and (cur+tl<len(t)):
                    key = tuple(t[cur:cur+tl+1])
                    if (key in GB_map) and (GB_map[key] >= apptime_thres):
                        tl += 1
                    else:
                        break
                res.append(' '.join(t[cur:cur + tl]))
                cur += tl
        return res


    def ir(self, pname, lm=20):
        '''
        retrieve data from Spotify server via its Python API
        :param pname: type: string, which is the partial or full name for the targeted tracks
        :param lm: type: integer, which is to define the up-limit for the number of retrieved tracks per function-call
        :return: res as as string list, which includes tracks' web-links with name piece as the input pname
        '''
        try:
            cur, res = 0, []
            ires = self.sp.search(q='track:' + pname, type='track', limit=lm, offset=0)
            while ires:
                p, cur = ires['tracks']['items'], cur+20
                for track in p: res.append(track['external_urls']['spotify'])
                if len(p) == 20: ires = self.sp.search(q='track:' + pname, type='track', limit=lm, offset=cur)
                else: break
            return res
        except: # Capture NetworkIO error
            return -1


def main():
    # Its function is to take a string as query input and print a list of URLs linking to result tracks.
    #
    try:
        opts = getopt.getopt(sys.argv[1:], "i:h", ["input","help"])
    except getopt.error:
        print "for help use --help"
        sys.exit(2)
    if (len(opts) != 2) or (opts[0][0] in ("-h", "--help")):
        print "Usage: python Spotify_IR.py -q 'California Hotel'"
        sys.exit(0)
    ir_engine = Spotify_IR()
    qpieces = ir_engine.name_shuffle(opts[0][0][1])
    for p in qpieces:
        res = ir_engine.ir(p)
        if res == -1:
            print 'Network IO ERROR!'
            sys.exit(3)
        for i in res:
            print i


if __name__ == "__main__":
    main()