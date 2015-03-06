# This file will pull everything together:
# Take and process command line args -> read in data -> encode data (potentially multiple times) -> transmit data
# OR  Take and process command line args -> use transmit module's retrieve method to grab data -> write out data

# get list of available modules
# TODO make this detect modules instaed of being manual
channelOptions = ['twitter']
encodingOptions = ['base64']

# command line arguments:
# you can input multiple transfer arguments, so -transfer and encoder will give a
# list of arguments. Need to change use encoder and use channel to loop
import argparse
parser = argparse.ArgumentParser(description = 'Use social media as a tool\
                                 for data exfiltration.')
parser.add_argument('--channel', '-c', dest = 'channelName', metavar="channel_name", action = 'store',
                             help = 'Choose a channel to transfer data over \
                             (e.g, --transfer twitter). Channels available: '+\
                             ", ".join(channelOptions), required = False) #change to True when done
parser.add_argument('--encode', '-e', dest = 'encoderNames', metavar="encoder_name", nargs='+', action = 'store',
                             help = 'Choose one or more methods of encoding (done in order given).\
                             Encoders available: ' + ", ".join(encodingOptions), required = False) #change to True when done

args = parser.parse_args()
d =  vars(args)
channelName = d.get('channelName')
encoderNames = d.get('encoderNames')

print channelName, encoderNames

# to use an encoder:
import importlib
encoderName = 'exampleEncoder'
moduleName = '.'.join(['encoders', encoderName])
enc = importlib.import_module(moduleName)
# This is a programmatic equivalent of:
# from encoding import exampleEncoder as enc

ret = enc.encode('this is my data')
print(ret)


# to use a channel:
channelName = 'exampleChannel'
moduleName = '.'.join(['channels', channelName])
chan = importlib.import_module(moduleName)

# send some stuff
chan.send("some data")

# receive some stuff
ret = chan.receive()
print(ret)
