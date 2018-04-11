import random

"""
Using `random` package for random number generation. 
This is to keep in line with the implementation in the DEAP library.
Note that `random.randint` has inclusive lower and upper bounds 
(differs from `np.random.randint`). 
"""

tec_template = {
    'T_coll': {'type': 'float',
               'min': 50.0,
               'max': 2000.0,
               'mutation': {
                   'probability': 0.25,
                   'mean': 0,
                   'std': 0.5
               }},
    'T_em': {'type': 'float',
             'min': 50.0,
             'max': 2000.0,
             'mutation': {
                 'probability': 0.25,
                 'mean': 0,
                 'std': 0.5
             }},
    'V_grid': {'type': 'float',
               'min': 0.0,
               'max': 20.0,
               'mutation': {
                   'probability': 0.25,
                   'mean': 0,
                   'std': 0.5
               }},
    'gap_distance': {'type': 'float',
                     'min': 1e-6,
                     'max': 20e-6,
                     'mutation': {
                         'probability': 0.25,
                         'mean': 0,
                         'std': 0.5
                     }},
    'grid_height': {'type': 'float',
                    'min': 0.05,
                    'max': 0.95,
                    'mutation': {
                        'probability': 0.25,
                        'mean': 0,
                        'std': 0.5
                    }},
    'phi_coll': {'type': 'float',
                 'min': 0.3,
                 'max': 4.0,
                 'mutation': {
                     'probability': 0.25,
                     'mean': 0,
                     'std': 0.5
                 }},
    'phi_em': {'type': 'float',
               'min': 0.3,
               'max': 4.0,
               'mutation': {
                   'probability': 0.25,
                   'mean': 0,
                   'std': 0.5
               }},
    'rho_cw': {'type': 'float',
               'min': 1e-5,
               'max': 1e-2,
               'mutation': {
                   'probability': 0.25,
                   'mean': 0,
                   'std': 0.5
               }},
    'rho_ew': {'type': 'float',
               'min': 1e-5,
               'max': 1e-2,
               'mutation': {
                   'probability': 0.25,
                   'mean': 0,
                   'std': 0.5
               }},
    'rho_load': {'type': 'float',
                 'min': 1e-4,
                 'max': 0.1,
                 'mutation': {
                     'probability': 0.25,
                     'mean': 0,
                     'std': 0.5
                 }},
    'strut_height': {'type': 'float',
                     'min': 10e-9,
                     'max': 20e-9,
                     'mutation': {
                         'probability': 0.25,
                         'mean': 0,
                         'std': 0.5
                     }},
    'strut_width': {'type': 'float',
                    'min': 10e-9,
                    'max': 20e-9,
                    'mutation': {
                        'probability': 0.25,
                        'mean': 0,
                        'std': 0.5
                    }},
    'x_struts': {'type': 'int',
                 'min': 1,
                 'max': 4,
                 'mutation': {
                     'probability': 0.25,
                     'lower': 1,
                     'upper': 5
                 }},
    'y_struts': {'type': 'int',
                 'min': 1,
                 'max': 4,
                 'mutation': {
                     'probability': 0.25,
                     'lower': 1,
                     'upper': 5
                 }}
}


def initDict(container, func):
    return func(container())


def generate_new_tec(adict, template=tec_template):
    for key, value in template.iteritems():
        value_type = template[key]['type']
        minimum, maximum = template[key]['min'], template[key]['max']

        if value_type == 'int':
            gen_num = random.randint(minimum, maximum)
        elif value_type == 'float':
            gen_num = minimum + random.random() * (maximum - minimum)
        else:
            raise TypeError("Type must be int or float")
        adict[key] = gen_num

    return adict


def mutIntorGauss(individual, template=tec_template):
    for key in individual:
        if template[key]['type'] == 'int':
            indpbInteger = template[key]['mutation']['probability']
            if random.random() < indpbInteger:
                xl, xu = template[key]['mutation']['lower'], template[key]['mutation']['upper']
                individual[key] = random.randint(xl, xu)
        if template[key]['type'] == 'float':
            indpbGauss = template[key]['mutation']['probability']
            if random.random() < indpbGauss:
                m, s = template[key]['mutation']['mean'], template[key]['mutation']['std']
                if random.random() < 0.5:
                    sgn = -1.0
                else:
                    sgn = +1.0
                individual[key] = abs(individual[key] + sgn * random.gauss(m, s))
    return individual,


def cxUniform(ind1, ind2, prob=0.5, template=tec_template):
    # TODO: What should prob be set to? Probability for any given gene to crossover if two individuals do cross over
    """
    Execute a gene level cross over with probability of prob for any given gene mutation.
    """
    k1, k2, r1, r2 = [random.uniform(0, 1) for _ in range(3)]
    for key in ind1:
        if random.random() < prob:
            S1, S2 = (1. + r1) * (k1 * ind1[key] + (1. - k1) * ind2[key]), \
                     (1. + r2) * (k2 * ind1[key] + (1. - k2) * ind2[key])
            if S1 < template[key]['min'] or S1 > template[key]['max']:
                S1 = S1 / (1. + r1)
            if S2 < template[key]['min'] or S2 > template[key]['max']:
                S2 = S2 / (1. + r1)
            if template[key]['type'] == 'int':
                ind1[key], ind2[key] = int(S1), int(S2)
            else:
                ind1[key], ind2[key] = int(S1), int(S2)

    return ind1, ind2