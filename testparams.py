from collections import OrderedDict
import pickle, sys

d = OrderedDict()
d['test1'] = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
d['test2'] = ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O")

params = {}
params['votefilepath'] = ("environ['USERPROFILE']", "'vote.dat'")
params['requiredChoices'] = 3
params['categories'] = d
params['hideVoteFile'] = False
params['allowRunning'] = True
params['overwriteVote'] = True

try:
    with open("paramtest.dat", 'wb') as f:
        pickle.dump(params, f, pickle.HIGHEST_PROTOCOL)
    print("write successful")
except Exception as e:
    print("an error occured ({0})".format(e), file=sys.stderr)

input("Press enter to finish")
