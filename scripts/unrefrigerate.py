import sys
import main.models
import pickle

print('Warning: this script is untested and probably won\'t work!')

def run():
    names = sys.argv[1:]

    for name in names:
        file = open('refrigerated-' + name + 's.pickled', 'r')
        models = pickle.load(models, file)
        map(lambda model: model.save(), models)
        