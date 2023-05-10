import MarkovInputData as D

class MatrixSupport:
    def __init__(self, transition_prob_matrix):
        """ initiates a patient
        :param transition_prob_matrix: transition probability matrix
        """
        self.transProbMatrix = transition_prob_matrix

    # raise awareness by a given number of percentage points
    def raiseAwareness(self, percentage_points):
        """
        :param percentage_points: number of percentage points by which to raise awareness
        """

        # raise awareness (P12) by stated number of percentage points
        self.transProbMatrix[D.HealthStates.RECOGNIZE_AMI.value][D.HealthStates.SEEK_HELP.value] \
            += percentage_points/100

        # when p12=0.536, 45% of people don't seek help
        # for every one percentage point increase in p12, the percentage of people not seeking help falls by one
        # percentage point
        non_help_seekers = 0.45 - \
                           (self.transProbMatrix[D.HealthStates.RECOGNIZE_AMI.value][D.HealthStates.SEEK_HELP.value] -
                            0.536)

        # The authors miscalculate P11 in their model (they set it to 0.1300 instead of 0.1305), so we need to set
        # P11 to the authors' value if we're in the baseline scenario. Otherwise, we calculate P11 by assuming
        # 29% of individuals who don't seek help prefer to manage their challenges alone
        if self.transProbMatrix[D.HealthStates.RECOGNIZE_AMI.value][D.HealthStates.SEEK_HELP.value] == 0.536:
            self.transProbMatrix[D.HealthStates.RECOGNIZE_AMI.value][D.HealthStates.DO_SOMETHING.value] = 0.13
        else:
            self.transProbMatrix[D.HealthStates.RECOGNIZE_AMI.value][D.HealthStates.DO_SOMETHING.value]\
                = 0.29 * non_help_seekers

        # individuals who don't seek help and also don't manage their challenges remain in the recognize AMI state
        self.transProbMatrix[D.HealthStates.RECOGNIZE_AMI.value][D.HealthStates.RECOGNIZE_AMI.value] \
            = non_help_seekers \
              - self.transProbMatrix[D.HealthStates.RECOGNIZE_AMI.value][D.HealthStates.DO_SOMETHING.value]


    # raise access by a given number of percentage points
    def raiseAccess(self, percentage_points):
        """
        :param percentage_points: number of percentage points by which to raise access
        """
        # raise access by stated number of percentage points
        self.transProbMatrix[D.HealthStates.SEEK_HELP.value][D.HealthStates.GET_HELP.value] \
            += percentage_points / 100

        # reduce probability of returning to recognize AMI state by stated number of percentage points
        self.transProbMatrix[D.HealthStates.SEEK_HELP.value][D.HealthStates.RECOGNIZE_AMI.value] \
            -= percentage_points / 100

