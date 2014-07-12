import sys
import main.models
import pickle

print('Warning: this script is untested and probably won\'t work!')

def run():
    names = sys.argv[1:]

    for name in names:
        models = list(main.models.__dict__[name].objects.all())
        pickle.dump(models, open('refrigerated-' + name + 's.pickled', 'w'))