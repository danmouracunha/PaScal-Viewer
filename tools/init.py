import util
import os
from util import Profiler as profiler
directory = os.getcwd()


with open('{}/freqmine.json'.format(directory), 'r') as file:
    profiler = util.Profiler(file)

    print(profiler.regions[0].get_efficiency())
