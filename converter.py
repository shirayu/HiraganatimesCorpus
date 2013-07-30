#!/usr/bin/python
# -*- coding: utf-8 -*- 


__author__ = 'Yuta Hayashibe' 
__version__ = ""
__copyright__ = ""
__license__ = "GPL v3"

"""
- The format changes between 2011.01 and 2011.02
- In the new format, English comes first, but may be multiline.
"""

import sys
import optparse
import codecs
import os.path

def load_from_stdin():
    in_encoding = sys.stdin.encoding
    if in_encoding is None:
        in_encoding = u"utf8"

    data = []
    for line in iter(sys.stdin.readline, ""):
        line = unicode(line.rstrip(), in_encoding)
        data.append(line)
    return data


def output(f_out, eng, jpn, name, lid):
    f_out.write(u"%s\t%s" % (name, lid))
    f_out.write(u"\t")

    f_out.write(eng)
    f_out.write(u"\t")

    f_out.write(jpn)

    f_out.write(u"\n")



def _convert_format_0(fname, fileid, f_out, f_out_multi, encode="cp932"):
    def is_multi_lines(eng, jpn):
        kuten_position = jpn.find(u"。") 
        if kuten_position !=-1 and (kuten_position!= len(jpn)-1):
            return True
        return False


    with codecs.open(fname, 'r', encode) as f:
        for lid, line in enumerate(f):
            sep_pos = line.find(u"●")
            if sep_pos != -1:
                eng = line[:sep_pos].lstrip().rstrip().replace(u"\t", u" ")
                jpn = line[sep_pos+1:].lstrip().rstrip().replace(u"\t", u" ")

                if eng == u"英文なし" or jpn == u"和訳なし" \
                    or jpn == u"（和訳なし）" \
                    or len(eng) == 0 or len(jpn) == 0:
                    continue

                if is_multi_lines(eng, jpn):
                    output(f_out_multi, eng, jpn, fileid, lid)
                else:
                    output(f_out, eng, jpn, fileid, lid)

def is_English(line):
    ascii_char_count = 0
    for char in line:
        if ord(char) <= 128:
            ascii_char_count += 1
    ratio = ascii_char_count / float(len(line))
    if ratio > 0.9:
        return True
#        print len(line), ascii_char_count, line.encode("utf8"), ratio
    return False



import nltk.tokenize
import re
jp_sent_tokenizer = nltk.tokenize.RegexpTokenizer(u'[^。]+。')
def _convert_format_1(fname, fileid, f_out, f_out_multi, encode="cp932"):

    def getLines(pair):
        eng = pair[0]
        jpn = pair[1]
        eng_lines = []
        jpn_lines = []

        tmp_eng_lines = nltk.tokenize.sent_tokenize(eng)
        tmp_jpn_lines = jp_sent_tokenizer.tokenize(jpn)

        if len(tmp_eng_lines) == len(tmp_jpn_lines):
            return tmp_eng_lines, tmp_jpn_lines
        else:
            #FIXME Ignore if the number of sentence are not equal
            pass

        return eng_lines, jpn_lines
        

    #==== MAIN ===
    last_line_id = 0
    pairs = [[]   ]
    for line in codecs.open(fname, 'r', encode):
        line = line.lstrip().rstrip()
        if line.startswith(u"〓〓〓"):
            pass
        elif len(line) == 0:
            #Note: sometimes blank line appears suddenly eg: line 207 @ 201103
            pass
        elif is_English(line):
            last_pair = pairs[-1]
            if len(last_pair) >= 2:
                pairs.append([line])
            else:
                last_pair.append(line)
        else: #Assume this line is written in Japanese
            #Sometimes this line ends with 〓
            trash_char_pos = line.find(u"〓")
            if trash_char_pos != -1:
                line = line[:trash_char_pos]

            last_pair = pairs[-1]
            last_pair.append(line)

    for pair in pairs:
        if len(pair) == 2 :
            eng_lines, jpn_lines = getLines(pair)
            for lid, el in enumerate(eng_lines):
                jl = jpn_lines[lid]
                output(f_out, el, jl, fileid, 0)
        else:
            #Ignore separated lines
            pass #FIXME


def convert(files, ofname):
    f_out = codecs.open(ofname , 'w', 'utf8')
    f_out_multi = codecs.open(ofname + u".multi", 'w', 'utf8')

    for fname in files:
        assert isinstance(fname, unicode)

        f_basename = os.path.basename(fname)
        if not f_basename.startswith(u"HT") or \
                not f_basename.endswith(u".TXT"):
            sys.stderr.write("Filename Error\n")
        fileid = f_basename[2:-4]
        fileid = int(fileid)

        if fileid < 201102:
            _convert_format_0(fname, fileid, f_out, f_out_multi)
        else:
            _convert_format_1(fname, fileid, f_out, f_out_multi)

    f_out.close()
    f_out_multi.close()


if __name__ == "__main__":
    argvs = sys.argv
    argc = len(argvs)
    INCODE = 'utf-8'

    in_encoding = sys.stdin.encoding
    if in_encoding is None:
        in_encoding = u"utf8"

    output_fname = unicode(sys.argv[1], in_encoding)
    if sys.argv[2] == "-":
        in_files = load_from_stdin()
    else:
        in_files = [unicode(_ofname, in_encoding) for _ofname in sys.argv[2:]]

    convert(in_files, output_fname)


