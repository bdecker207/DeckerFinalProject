from enum import Enum

# simulation settings
POP_SIZE = 500000         # cohort population size
ALPHA = 0.05

class HealthStates(Enum):
    """ health states of patients with AMI """
    RECOGNIZE_AMI = 0
    SEEK_HELP = 1
    GET_HELP = 2
    DO_SOMETHING = 3
    SUICIDE = 4
    GET_BETTER = 5


# transition matrix
TRANS_PROB_MATRIX = [
    [0.320, 0.536, 0.000, 0.130, 0.014, 0.000],   # RECOGNIZE_AMI
    [0.124, 0.000, 0.862, 0.000, 0.014, 0.000],   # SEEK_HELP
    [0.100, 0.000, 0.043, 0.043, 0.014, 0.800],   # GET_HELP
    [0.329, 0.000, 0.000, 0.328, 0.014, 0.329],   # DO_SOMETHING
    [0.000, 0.000, 0.000, 0.000, 1.000, 0.000],   # SUICIDE
    [0.000, 0.000, 0.000, 0.000, 0.000, 1.000],   # GET_BETTER
    ]

# transition matrix
TRANS_PROB_MATRIX_2 = [
    [0.320, 0.536, 0.000, 0.130, 0.014, 0.000],   # RECOGNIZE_AMI
    [0.105, 0.000, 0.881, 0.000, 0.014, 0.000],   # SEEK_HELP
    [0.100, 0.000, 0.068, 0.068, 0.014, 0.750],   # GET_HELP
    [0.329, 0.000, 0.000, 0.328, 0.014, 0.329],   # DO_SOMETHING
    [0.000, 0.000, 0.000, 0.000, 1.000, 0.000],   # SUICIDE
    [0.000, 0.000, 0.000, 0.000, 0.000, 1.000],   # GET_BETTER
    ]