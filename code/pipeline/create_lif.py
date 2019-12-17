"""create_lif.py

Create LIF files from the JSON files. The format of those files is similar to
the format of Science Parse output.

Usage:

$ python create_lif.py -d DATA_DIR -f FILE_LIST -s START -e END

The -d and -f options are there to hand in the directory to be processed and a
file list with relative file paths in that directory. DATA_DIR is assumed to
have a sub directory jsn with the JSON files and the file paths in there are
listed in FILE_LIST. New directories lif and txt will be created (if they exist,
contents may be overwritten) and after running this script those directory will
have the same structure as jsn.

"""


import os
import sys
import json
import traceback
from getopt import getopt
from io import StringIO

from lif import LIF, Container, View, Annotation
from utils import time_elapsed, elements, ensure_directory


@time_elapsed
def process_filelist(data_dir, filelist, start, end, crash=False):
    for n, fname in elements(filelist, start, end):
        if crash:
            process_list_element(data_dir, n, fname)
        else:
            try:
                process_list_element(data_dir, n, fname)
            except Exception as e:
                sys.stderr.write("ERROR on %07d  %s\n" % (n, fname))
                print('ERROR:', Exception, e)


def process_list_element(data_dir, n, fname):
    print("%07d  %s" % (n, fname))
    jsn_file = os.path.join(data_dir, 'jsn', fname)
    lif_file = os.path.join(data_dir, 'lif', fname[:-4] + 'lif')
    txt_file = os.path.join(data_dir, 'txt', fname[:-4] + 'txt')
    ensure_directory(lif_file, txt_file)
    create_lif_file(jsn_file, lif_file, txt_file)


def create_lif_file(json_file, lif_file, txt_file, test=False):
    #print("Creating {}".format(lif_file))
    with open(json_file, encoding='utf8') as fh_in, \
         open(lif_file, 'w', encoding='utf8') as fh_out_lif, \
         open(txt_file, 'w', encoding='utf8') as fh_out_txt:
        json_obj = json.loads(fh_in.read())
        lif_obj = LIF()
        _add_metadata(lif_obj, json_obj)
        _add_view(lif_obj, json_obj)
        _add_rest(lif_obj, json_obj)
        container = Container()
        container.discriminator = "http://vocab.lappsgrid.org/ns/media/jsonld#lif"
        container.payload = lif_obj
        fh_out_lif.write(json.dumps(container.as_json(), indent=4))
        fh_out_txt.write(container.payload.text.value)
    if test:
        test_lif_file(lif_file)


def _add_metadata(lif_obj, json_obj):
    lif_obj.metadata['id-pmc'] = json_obj['id-pmc']
    lif_obj.metadata['id-pmid'] = json_obj['id-pmid']
    lif_obj.metadata['authors'] = json_obj['authors']
    lif_obj.metadata['title'] = json_obj.get('title')
    lif_obj.metadata['year'] = json_obj.get('year')
    lif_obj.metadata['references'] = json_obj['references']


def _add_view(lif_obj, json_obj):
    view = View()
    lif_obj.views.append(view)
    view.id = "structure"
    view.metadata['contains'] = { vocab("Title"): {}, vocab("Abstract"): {},
                                  vocab("Section"): {}, vocab("Header"): {} }


def _add_rest(lif_obj, json_obj):
    text_value = StringIO()
    offset = 0
    annotations = lif_obj.views[0].annotations
    offset = _add_annotation(annotations, text_value, 'Title', json_obj.get('title'), offset)
    offset = _add_annotation(annotations, text_value, 'Abstract', json_obj.get('abstractText'), offset)
    for section in json_obj['sections']:
        offset = _add_annotation(annotations, text_value, 'Header', section.get('heading'), offset)
        offset = _add_annotation(annotations, text_value, 'Section', section.get('text'), offset)
    lif_obj.text.value = text_value.getvalue()


def _add_annotation(annotations, text_value, annotation_type, text, offset):
    if text is None:
        return offset
    prefix = None
    if annotation_type in ('Title', 'Abstract'):
        prefix = annotation_type.upper()
    if prefix is not None:
        anno = {
            "id": IdentifierFactory.next_id('Header'),
            "@type": vocab('Header'),
            "start": offset,
            "end": offset + len(prefix) }
        annotations.append(Annotation(anno))
        text_value.write(prefix + u"\n\n")
        offset += len(prefix) + 2
    anno = {
        "id": IdentifierFactory.next_id(annotation_type),
        "@type": vocab(annotation_type),
        "start": offset,
        "end": offset + len(text) }
    annotations.append(Annotation(anno))
    text_value.write(text + u"\n\n")
    return offset + len(text) + 2


def test_lif_file(lif_file):
    """Just print the text of all headers, should give an indication of whether all
    the offsets are correct."""
    lif = Container(json_file=lif_file).payload
    text = lif.text.value
    view = lif.views[0]
    for anno in view.annotations:
        if anno.type.endswith('Header'):
            print("[{}]".format(text[anno.start:anno.end]))
    print('')


class IdentifierFactory(object):

    ids = { 'Title': 0, 'Abstract': 0, 'Header': 0, 'Section': 0 }

    @classmethod
    def next_id(cls, tagname):
        cls.ids[tagname] += 1
        return "{}{:04d}".format(tagname.lower(), cls.ids[tagname])


def vocab(annotation_type):
    return "http://vocab.lappsgrid.org/{}".format(annotation_type)


def usage():
    print("\nUsage:\n"
          + "\n    $ python3 convert_nxml.py -d DATA_DIR -f FILELIST"
          + "\n    $ python3 convert_nxml.py -d DATA_DIR -f FILELIST -s START -e END"
          + "\n    $ python3 convert_nxml.py -d DATA_DIR -f FILELIST --crash"
          + "\n    $ python3 convert_nxml.py (-h | --help)\n")


if __name__ == '__main__':

    data_dir = '/DATA/eager/sample-01000'
    filelist = '../../data/files-random-01000.txt'

    options = dict(getopt(sys.argv[1:], 'd:f:s:e:h', ['crash', 'help'])[0])
    print(options)
    data_dir = options.get('-d', data_dir)
    filelist = options.get('-f', filelist)
    start = int(options.get('-s', 1))
    end = int(options.get('-e', 1))
    crash = True if '--crash' in options else False
    help_wanted = True if '-h' in options or '--help' in options else False

    if help_wanted:
        usage()
    else:
        process_filelist(data_dir, filelist, start, end, crash=crash)

