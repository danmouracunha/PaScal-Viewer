import json

import numpy as np
from numpy import median


class ReadingFormat(object):
    ARGUMENTS_PER_THREADS = 0
    THREADS_PER_ARGUMENTS = 1


class Region:
    def __init__(self, filename, initial_line, final_line, executions_data, reading_format):
        self.filename = filename
        self.initial_line = initial_line
        self.final_line = final_line
        self.executions_data = executions_data
        self.reading_format = reading_format

    def get_efficiency(self):
        def get_efficiency_arguments_per_threads():
            efficiency_data = []
            n_rows = 0
            for argument in self.executions_data.values():
                for thread in argument.values():
                    efficiency_data.append(median(thread['efficiencies']))
                n_rows += 1

            n_columns = int(len(efficiency_data) / n_rows)
            return np.reshape(efficiency_data, (n_rows, n_columns)).astype(np.float32)

        def get_efficiency_threads_per_arguments():
            return np.transpose(get_efficiency_arguments_per_threads())

        if self.reading_format == ReadingFormat.ARGUMENTS_PER_THREADS:
            return get_efficiency_arguments_per_threads()
        else:
            return get_efficiency_threads_per_arguments()

    def get_speedup(self):
        def get_speedup_arguments_per_threads():
            speedup_data = []
            n_rows = 0
            for argument in self.executions_data.values():
                for thread in argument.values():
                    speedup_data.append(median(thread['speedups']))
                n_rows += 1

            n_columns = int(len(speedup_data) / n_rows)
            return np.reshape(speedup_data, (n_rows, n_columns)).astype(np.float32)

        def get_speedup_threads_per_arguments():
            return np.transpose(self.get_speedup_arguments_per_threads())

        if self.reading_format == ReadingFormat.ARGUMENTS_PER_THREADS:
            return get_speedup_arguments_per_threads()
        else:
            return get_speedup_threads_per_arguments()

    def get_scalability_on_rows(self):
        matrix = self.get_efficiency()
        
        result = (matrix.transpose()[1:]- matrix.transpose()[:-1]).transpose()
        # a = []
        # a = np.pad(result, ((0,0),(1,0)), 'constant')
        return result
        

    def get_scalability_on_columns(self):
        matrix = self.get_efficiency()
        
        result = matrix[1:] - matrix[:-1]
        # a = []
        # a = np.pad(result, ((1,0),(0,0)), 'constant')
        
        return result

    def get_scalability_on_diagonals(self):
        matrix = self.get_efficiency()
        
        result = (matrix[1:].transpose()[1:] - matrix[:-1].transpose()[:-1]).transpose()
        # a = []
        # a = np.pad(result, ((1,0),(1,0)), 'constant')
        return result

    def get_header_arguments(self):
        return list(self.executions_data.keys())

    def get_header_threads(self):
        return list(list(self.executions_data.values())[0].keys())

    def get_scalability_on_columns_from_idealvariation(self):
        matrix = self.get_efficiency()
        n_rows = np.size(matrix, 0)
        n_columns = np.size(matrix, 1)
        new_matrix = np.zeros((n_rows, n_columns))
        for column in range(n_columns):
            for row in range(n_rows):
                new_matrix[row, column] = 1. - matrix[row, column]
        return new_matrix
    def get_scalability_on_rows_from_idealvariation(self):
        matrix = self.get_efficiency()
        new_matrix = []
        n_rows = np.size(matrix, 0)
        n_columns = np.size(matrix, 1)
        for row in matrix:
            for i in range(0, len(row)):
                value = 1. - row[i]
                new_matrix.append(value)
        return np.reshape(new_matrix, (n_rows, n_columns)).astype(np.float32)


class Profiler:
    def __init__(self, data_file):
        try:
            data = json.load(data_file)
        except:
            print("haha")
            data = data_file

        # get data regions
        self.header_arguments = None
        self.header_threads = None
        self.regions = []

        for region in data:
            filename = region['filename']
            initial_line, final_line = region['region'].split(', ')
            if initial_line == 0 and final_line == 0:
                self.appname = filename

            executions_data = {}

            # reading all executions of this region
            executions = region['executions']
            for execution in executions:
                n_threads = []
                arguments = []

                for runs_per_exec in execution:
                    argument = runs_per_exec['argument']
                    runs = runs_per_exec['runs']

                    arguments.append(argument)
                    if argument not in executions_data:
                        executions_data[argument] = {}

                    base_time = 0
                    for run in runs:
                        threads = run['threads']
                        time = float(run['time'])

                        if threads == 1:
                            base_time = time

                        speedup = float(base_time / time)

                        if threads not in executions_data[argument]:
                            executions_data[argument][threads] = {}
                            executions_data[argument][threads]['times'] = []
                            executions_data[argument][threads]['speedups'] = []
                            executions_data[argument][threads]['efficiencies'] = []

                        executions_data[argument][threads]['times'].append(time)
                        executions_data[argument][threads]['speedups'].append(speedup)
                        executions_data[argument][threads]['efficiencies'].append(speedup / int(threads))

                        n_threads.append(threads)

                # add column headers
                if not self.header_threads:
                    n_threads = list(dict.fromkeys(n_threads).keys())
                    self.header_threads = n_threads

                # add row headers
                if not self.header_arguments:
                    self.header_arguments = arguments

            # create region
            self.regions.append(Region(filename, initial_line, final_line,
                                       executions_data, ReadingFormat.THREADS_PER_ARGUMENTS))
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
