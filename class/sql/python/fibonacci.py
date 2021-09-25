import os
import re
import json
import logging

LOG = logging.getLogger() 


# output_handler = logging.StreamHandler()
# formatter = CustomJsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# output_handler.setFormatter(formatter) 
# while len(LOG.handlers) > 0:
    # LOG.handlers.pop()
# LOG.addHandler(output_handler)
# deployment time, set the log level. [warning]
LOG.debug({"message":"fdsafs"})
LOG.info("fdsafs")
LOG.warning("fdsafs")
LOG.error("fdsafs")

def main(args):
    if os.path.isdir(args.files):
            files = os.listdir(args.files)
            files = [os.path.join(args.files, file) for file in files if os.path.splitext(file)[1] in ['.wav', '.flac']]
    else:
        files = args.files.split(',')
    files = files[:args.max]
    os.path.mkdir("temp")
    os.path.remov("tmp")
    pattern = "\"?[0-9a-zA-z]*?@\w+\.\w+\"?"
    re.compile(pattern)
    re.match("abc*def")
    
    json.load()
    str = json.dump(json)
    