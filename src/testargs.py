import sys
import os
import getopt

def process_args(argv):
   persist = False
   move = False
   debug=False
   stopCount=10

   try:
      opts, args = getopt.getopt(argv,"hd:c:p:m:",["debug=","stopcount=","persist=","move="])
   except getopt.GetoptError:
      print( 'test.py -d <shouldDebug> -p <shouldPersistLogs> -c <count> -m <shouldMove> ')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print( 'test.py -d <shouldDebug> -p <shouldPersistLogs> -c <count> -m <shouldMove> ')
         sys.exit()
      elif opt in ("-d", "--debug"):
         debug = bool(arg)
      elif opt in ("-c", "--stopcount"):
         stopCount = int(arg)
      elif opt in ("-p", "--persist"):
         persist = bool(arg)
      elif opt in ("-m", "--move"):
         move = bool(arg)
   print(persist ,move ,debug,stopCount)


process_args(sys.argv[1:])