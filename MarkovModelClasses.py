import numpy as np
from MarkovInputData import HealthStates
from deampy.markov import MarkovJumpProcess
import MarkovInputData as D
import deampy.statistics as stats

class Patient:
    def __init__(self, id, transition_prob_matrix):
        """ initiates a patient
        :param id: ID of the patient
        :param transition_prob_matrix: transition probability matrix
        """
        self.id = id
        self.transProbMatrix = transition_prob_matrix
        self.currentState = HealthStates.RECOGNIZE_AMI    # current health state

    def simulate(self):
        """ simulate the patient until an absorbing state is reached """

        # random number generator
        rng = np.random.RandomState(seed=self.id)
        # Markov jump process
        markov_jump = MarkovJumpProcess(transition_prob_matrix=self.transProbMatrix)

        k = 0  # simulation time step

        # while the patient is not in an absorbing state
        while self.currentState != HealthStates.SUICIDE and self.currentState != HealthStates.GET_BETTER:
            # sample from the Markov jump process to get a new state
            # (returns an integer from {0, 1, 2, ...})
            new_state_index = markov_jump.get_next_state(
                current_state_index=self.currentState.value,
                rng=rng)

            # update health state
            self.currentState = HealthStates(new_state_index)

            # increment time
            k += 1

class Cohort:
    def __init__(self, id, pop_size, transition_prob_matrix):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param transition_prob_matrix: transition probability matrix
        """
        self.id = id
        self.popSize = pop_size
        self.transitionProbMatrix = transition_prob_matrix
        self.cohortOutcomes = CohortOutcomes()  # outcomes of this simulated cohort

    def simulate(self):
        """ simulate the cohort of patients
        """
        # populate and simulate the cohort
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i,
                              transition_prob_matrix=self.transitionProbMatrix)
            # simulate
            patient.simulate()

            # store outputs of this simulation
            self.cohortOutcomes.extract_outcome(simulated_patient=patient)

        # calculate cohort outcomes for this simulation
        self.cohortOutcomes.calculate_cohort_outcomes()


class CohortOutcomes:
    def __init__(self):

        self.finalStates = [] # list of final states of patients
        self.suicideProportion = None # proportion of patients who commit suicide
        self.suicideProportionCI = None # CI of proportion of patients who commit suicide

    def extract_outcome(self, simulated_patient):
        """ extracts outcomes of a simulated patient
        :param simulated_patient: a simulated patient"""

        # record patient's final state (1 for suicide, 0 for get better)
        if simulated_patient.currentState == D.HealthStates.SUICIDE:
            self.finalStates.append(1)
        elif simulated_patient.currentState == D.HealthStates.GET_BETTER:
            self.finalStates.append(0)
        else:
            print("Error")

    def calculate_cohort_outcomes(self):
        # create a summary statistics
        suicide_stat = stats.SummaryStat(name='Proportion of patients who commit suicide',
                                         data=self.finalStates)

        # get mean and confidence confidence interval
        self.suicideProportion = suicide_stat.get_mean()
        self.suicideProportionCI = suicide_stat.get_t_CI(alpha=D.ALPHA)


