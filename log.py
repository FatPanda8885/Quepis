import os
import datetime
import output



def setup():
    global formed_filename
    filename = str(datetime.datetime.now())+".txt"
    filename = filename.replace(":", "-")
    filename = filename.replace(" ", "_")
    formed_filename = filename
    with open(filename, 'a') as f:
        filename = os.path.basename(f.name)
        f.write("log start at "+formed_filename+"\n")
        output.info_output("Log System Setuping...")

def write_info(data):
    global formed_filename
    with open(formed_filename, 'a') as f:
        f.write("[INFO]("+str(datetime.datetime.now())+")"+data+" \n")

def write_error(data):
    global formed_filename
    with open(formed_filename, 'a') as f:
        f.write("[ERROR]("+str(datetime.datetime.now())+")"+data+" \n")

def write_warn(data):
    global formed_filename
    with open(formed_filename, 'a') as f:
        f.write("[WARN]("+str(datetime.datetime.now())+")"+data+" \n")
