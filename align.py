import argparse
import logging
import multiprocessing
import os
import sys

import json
import gentle
from datetime import timedelta

parser = argparse.ArgumentParser(
        description='Align a transcript to audio by generating a new language model.  Outputs JSON')
parser.add_argument(
        '--nthreads', default=multiprocessing.cpu_count(), type=int,
        help='number of alignment threads')
parser.add_argument(
        '-o', '--output', metavar='output', type=str, 
        help='output filename')
parser.add_argument(
        '--conservative', dest='conservative', action='store_true',
        help='conservative alignment')
parser.set_defaults(conservative=False)
parser.add_argument(
        '--disfluency', dest='disfluency', action='store_true',
        help='include disfluencies (uh, um) in alignment')
parser.set_defaults(disfluency=False)
parser.add_argument(
        '--log', default="INFO",
        help='the log level (DEBUG, INFO, WARNING, ERROR, or CRITICAL)')
parser.add_argument(
        'audiofile', type=str,
        help='audio file')
parser.add_argument(
        'txtfile', type=str,
        help='transcript text file')
args = parser.parse_args()

log_level = args.log.upper()
logging.getLogger().setLevel(log_level)

disfluencies = set(['uh', 'um'])

def on_progress(p):
    for k,v in p.items():
        logging.debug("%s: %s" % (k, v))


with open(args.txtfile, encoding="utf-8") as fh:
    transcript = fh.read()

resources = gentle.Resources()
logging.info("converting audio to 8K sampled wav")

with gentle.resampled(args.audiofile) as wavfile:
    logging.info("starting alignment")
    aligner = gentle.ForcedAligner(resources, transcript, nthreads=args.nthreads, disfluency=args.disfluency, conservative=args.conservative, disfluencies=disfluencies)
    result = aligner.transcribe(wavfile, progress_cb=on_progress, logging=logging)

fh = open(args.output, 'w', encoding="utf-8") if args.output else sys.stdout
fh.write(result.to_json(indent=2))
if args.output:
    logging.info("output written to %s" % (args.output))
    

with open('/Users/anchalbhardwaj/Downloads/gentle-Final/sample.json') as f:
  data = json.load(f)
  
import sys
 
file_path = '/Users/anchalbhardwaj/Downloads/alignFinalHello.vtt'
sys.stdout = open(file_path, "w")
logging.info("starting vtt conversion")
  
def formatTime(oldtime):
    td = timedelta(seconds=oldtime)
    return str(0)+str(td)[:-3]

newTranscript = data["transcript"].split(" ")
def checkWord(pos):
    if (data["words"][pos]["word"] != newTranscript[pos]):
        return newTranscript[pos]
    else:
        return data["words"][pos]["word"]

print ("WEBVTT")

i = 0
while i < len(data["words"])-6:
    for x in range(int(len(data["words"])/7)):
        print("\n"+ str(x+1))
        print(str(formatTime(data["words"][i]["start"])+ " --> " + str(formatTime(data["words"][i+6]["end"]))))
        print(str(checkWord(i)) + " " + str(checkWord(i+1)) + " " + str(checkWord(i+2)) + " " + str(checkWord(i+3)) + " " + str(checkWord(i+4)) + " " + str(checkWord(i+5)) + " " + str(checkWord(i+6)))
        i = i + 7;
        
logging.info("finished vtt conversion")
