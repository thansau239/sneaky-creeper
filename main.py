import os
import pkgutil
import sys
import importlib
import argparse

<<<<<<< HEAD
# get list of available modules
# TODO make this detect modules instaed of being manual
channelOptions = ['twitter', 'googleDocs', 'exampleChannel']
encodingOptions = ['b64', 'exampleEncoder']
=======
# get all of the possible channels and encoders to load and use

# generate paths to the encoder and channel folders
currentDir = os.path.dirname(os.path.abspath(__file__))
channels = os.path.join(currentDir, 'channels')
encoders = os.path.join(currentDir, 'encoders')

channels = pkgutil.iter_modules(path=[channels])
encoders = pkgutil.iter_modules(path=[encoders])

# these are all of the modules available to be loaded and used
channelOptions = [modName for _,modName,_ in channels]
encodingOptions = [modName for _,modName,_ in encoders]
>>>>>>> master

# command line arguments:
# you can input multiple transfer arguments, so -transfer and encoder will give a
# list of arguments. Need to change use encoder and use channel to loop
parser = argparse.ArgumentParser(description = 'Use social media as a tool for data exfiltration.')
subparsers = parser.add_subparsers(dest='subcommand')


# subparser for encoder exploration
parser_encoders = subparsers.add_parser('encoders')
#parser_encoders.add_argument()

#  subparser for channel exploration
parser_channels = subparsers.add_parser('channels')
#parser_channels.add_argument()


# subparser for sending data
parser_send = subparsers.add_parser('send')
parser_send.add_argument('--channel', '-c', dest = 'channelName', metavar="channel_name", action = 'store',
                             help = 'Choose a channel to transfer data over \
                             (e.g, --transfer twitter).', required = True)

parser_send.add_argument('--encoder', '-e', dest = 'encoderNames', metavar="encoder_name", nargs='+', action = 'store',
                             help = 'Choose one or more methods of encoding (done in order given).', required=True)

parser_send.add_argument('--input', '-i', help = 'Specify a file to read from, or leave blank for stdin.',\
                             metavar = 'filename', type = argparse.FileType('r'), default = '-')

parser_send.add_argument('--parameters', '-p', dest = 'params', metavar="parameter_name", nargs='+', action = 'append',
                             help = 'Specify parameters as name-value pairs [-p name value] to be passed to encoder and channel modules.')


# subparser for fetching data
parser_receive = subparsers.add_parser('receive')
parser_receive.add_argument('--channel', '-c', dest = 'channelName', metavar="channel_name", action = 'store',
                             help = 'Choose a channel to transfer data over \
                             (e.g, --transfer twitter).', required = True)

parser_receive.add_argument('--encoder', '-e', dest = 'encoderNames', metavar="encoder_name", nargs='+', action = 'store',
                             help = 'Choose one or more methods of encoding (done in order given).', required=True)

parser_receive.add_argument('--parameters', '-p', dest = 'params', metavar="parameter_name", nargs='+', action = 'append',
                             help = 'Specify parameters as name-value pairs [-p name value] to be passed to encoder and channel modules.')

######### END ARG PARSER #########

def receiveData(channelName, params):
    # to use a channel:
    moduleName = '.'.join(['channels', channelName])
    chan = importlib.import_module(moduleName)

    # make sure we have all of the required parameters
    abort = False
    for param,desc in chan.requiredParams['receiving'].iteritems():
        if not param in params:
            print("ERROR: Missing required parameter \'{}\' for channel \'{}\'.".format(param, channelName))
            abort = True # so that multiple problems can be found in one run
    if(abort):
        sys.exit()

    # receive some stuff
    resp = chan.receive(params)
    return resp

def sendData(channelName, data, params):
    # ensure the passed modules are valid
    if not channelName in channelOptions:
        print("ERROR: channel " + channelName + " does not exist.")
        return

    # to use a channel:
    moduleName = '.'.join(['channels', channelName])
    chan = importlib.import_module(moduleName)

    # make sure we have all of the required parameters
    abort = False
    for param,desc in chan.requiredParams['sending'].iteritems():
        if not param in params:
            print("ERROR: Missing required parameter \'{}\' for channel \'{}\'.".format(param, channelName))
            abort = True # so that multiple problems can be found in one run
    if(abort):
        sys.exit()

    # send some stuff
    chan.send(data, params)

def encode(encoderNames, data, params):
    # encode some data by passing it through the given encoders
    # encoders are ASSUMED GOOD
    for encoderName in encoderNames:
        moduleName = '.'.join(['encoders', encoderName])
        enc = importlib.import_module(moduleName)
        # This is a programmatic equivalent of:
        # from encoding import exampleEncoder as enc

        # make sure we have all of the required parameters
        abort = False
        for param,desc in enc.requiredParams['encode'].iteritems():
            if not param in params:
                print("ERROR: Missing required parameter \'{}\' for encoder \'{}\'.".format(param, encoderName))
                abort = True # so that multiple problems can be found in one run
        if(abort):
            sys.exit()

        data = enc.encode(data, params)

    return data

def decode(encoderNames, data):
    # decode some data by passing it through the given encoders, in reverse
    # i.e. [enc1, enc2] means data is decoded by enc2, then enc1
    # This allows decoders to be specified in the same order on both ends, and still work.
    for encoderName in reversed(encoderNames):
        moduleName = '.'.join(['encoders', encoderName])
        enc = importlib.import_module(moduleName)
        # This is a programmatic equivalent of:
        # from encoding import exampleEncoder as enc

        # make sure we have all of the required parameters
        abort = False
        for param,desc in enc.requiredParams['decode'].iteritems():
            if not param in params:
                print("ERROR: Missing required parameter \'{}\' for encoder \'{}\'.".format(param, encoderName))
                abort = True # so that multiple problems can be found in one run
        if(abort):
            sys.exit()

        data = enc.decode(data, params)

    return data

def encoders():
    # Do everything to handle the 'encoders' subcommand.
    print("Currently available encoders:")
    print('    ' + ', '.join(encodingOptions))
    return

def channels():
    # Do everything to handle the 'channels' subcommand.
    print("Currently available channels:")
    print('    ' + ', '.join(channelOptions))
    return

############## RUN ##############
args = parser.parse_args()
d =  vars(args)

if args.subcommand == 'encoders':
    encoders()

if args.subcommand == 'channels':
    channels()

if args.subcommand == 'send':
    channelName = d.get('channelName')
    encoderNames = d.get('encoderNames')
    params = d.get('params')
    data = d.get('input').read() # either a given file, or stdin

    #write a for loop that adds the params to a dictionary called params, then delete the foo bar dict
    paramd = {}
    if params:
        for param in range(len(params)):
            paramd[params[param][0]] = params[param][1]

    # check the encoders all exist
    for encoderName in encoderNames:
        if not encoderName in encodingOptions:
            print("ERROR: encoder " + encoderName + " does not exist. Exiting.")
            sys.exit()

    # check the channel exists
    if not channelName in channelOptions:
        print("ERROR: channel " + channelName + " does not exist. Exiting.")
        sys.exit()

    # tell the user what we're going to do
    print("")
    print("Pipeline: " + "-> ".join(encoderNames) + "-> " + channelName)
    print("")


    encoded = encode(encoderNames, data, paramd)
    sendData(channelName, encoded, paramd)

if args.subcommand == 'receive':
    channelName = d.get('channelName')
    encoderNames = d.get('encoderNames')
    params = d.get('params')

    paramd = {}
    if params:
        for param in range(len(params)):
            paramd[params[param][0]] = params[param][1]

    # check the encoders all exist
    for encoderName in encoderNames:
        if not encoderName in encodingOptions:
            print("ERROR: encoder " + encoderName + " does not exist. Exiting.")
            sys.exit()

    # check the channel exists
    if not channelName in channelOptions:
        print("ERROR: channel " + channelName + " does not exist. Exiting.")
        sys.exit()

    data = receiveData(channelName, paramd)

    #this will be useful code later when we have multiple messages to decode

    #for datam in range(len(data)):
    #    datar = str(data[datam])
    #    output = decode(encoderNames, datar)

    output = decode(encoderNames, str(data[0]))
    sys.stdout.write(str(output))
