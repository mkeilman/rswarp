import h5py as h5
import numpy as np
import os
import re


def _printname(name):
    print name


def explore(filename):
    f = h5.File(filename, 'r')

    return f.visit(_printname)

def cleanupPrevious(particleDirectory, fieldDirectory):

    """
    Remove old diagnostic files.

    Parameters:
            particleDirectory (str): Path to particle diagnostics

    """
    if os.path.exists(particleDirectory):
        files = os.listdir(particleDirectory)
        for file in files:
            if file.endswith('.h5'):
                os.remove(os.path.join(particleDirectory,file))
    if isinstance(fieldDirectory,dict):
        for key in fieldDirectory:
            if os.path.exists(fieldDirectory[key]):
                files = os.listdir(fieldDirectory[key])
                for file in files:
                    if file.endswith('.h5'):
                        os.remove(os.path.join(fieldDirectory[key],file))
    elif isinstance(fieldDirectory, list):
        for directory in fieldDirectory:
            if os.path.exists(directory):
                files = os.listdir(directory)
                for file in files:
                    if file.endswith('.h5'):
                        os.remove(os.path.join(directory, file))
    elif isinstance(fieldDirectory, str):
            if os.path.exists(fieldDirectory):
                files = os.listdir(fieldDirectory)
                for file in files:
                    if file.endswith('.h5'):
                        os.remove(os.path.join(fieldDirectory, file))


def readparticles(filename):
    """
    Reads in openPMD compliant particle file generated by Warp's ParticleDiagnostic class.

    Parameters:
        filename (str): Path to a ParticleDiagnostic output file.
    Returns:
        particle_arrays (dict): Dictionary with entry for each species in the file that contains an array
         of the 6D particle coordinates.
    """

    dims = ['momentum/x', 'position/y', 'momentum/y', 'position/z', 'momentum/z']
    particle_arrays = {}

    f = h5.File(filename, 'r')

    if f.attrs.get('openPMD') is None:
        print "Warning!: Not an openPMD file. This may not work."

    step = f['data'].keys()[0]
    time = f['data/%s' % step].attrs["time"]
    dt = f['data/%s' % step].attrs["dt"]

    species_list = f['data/%s/particles' % step].keys()

    for species in species_list:
        parray = f['data/%s/particles/%s/position/x' % (step, species)]
        for dim in dims:
            parray = np.column_stack((parray, f['data/%s/particles/%s/' % (step, species) + dim]))

        particle_arrays[species] = parray
        particle_arrays['time'] = time
        particle_arrays['dt'] = dt

    return particle_arrays


def loadparticlefiles(directory):
    """
    Loads all particle diagnostic files from a directory using readparticles() and loads to a dictionary of the files.
    Parameters (str):
        directory: Path to a directory containing ParticleDiagnostic output files.
    Returns (dict): Dictionary containing output of each file in the directory.
    """
    #Returns runData dictionary with particle coorinates for each file in directory

    step_arrays = {}

    for obj in os.listdir(directory):
        file_path = os.path.join(directory, obj)
        if os.path.isfile(file_path) and os.path.splitext(obj)[1] == '.h5':

            step = int(re.findall(r'\d+', obj)[0])

            step_arrays[step] = readparticles(directory + obj)

    return step_arrays
