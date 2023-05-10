import deampy.statistics as stats
import MarkovInputData as D

class CohortComparison:

    def __init__(self):
        self.rateIncrease = None # Increase in suicide rate between cohorts
        self.rateIncreaseCI = None # 95% CI for increase in suicide rate between cohorts

    def compare_outcomes(self, cohort_1, cohort_2):
        """ prints expected increase in average suicide rate between cohorts
        :param cohort_1: first cohort
        :param cohort_2: second cohort
        """
        # increase in proportion of patients who commit suicide
        increase_stat = stats.DifferenceStatIndp(
            x=cohort_2.cohortOutcomes.finalStates,
            y_ref=cohort_1.cohortOutcomes.finalStates)

        # mean and confidence interval
        self.rateIncrease = increase_stat.get_mean()
        self.rateIncreaseCI = increase_stat.get_t_CI(alpha=D.ALPHA)



def print_outcomes(cohort, strategy_name):
    """ prints the outcomes of a simulated cohort under steady state
    :param cohort: a simulatecohort
    :param strategy_name: the name of the selected therapy
    """

    # create a summary statistics
    suicide_stat = stats.SummaryStat(name='Proportion of patients who commit suicide',
                                        data=cohort.cohortOutcomes.finalStates)

    # get mean and confidence confidence interval
    mean = suicide_stat.get_mean()
    conf_int = suicide_stat.get_t_CI(alpha=D.ALPHA)

    # print survival time statistics
    print(strategy_name)
    print("  Estimate of proportion of patients who commit suicide and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0), mean, conf_int)

def print_comparative_outcomes(cohort_1, cohort_2):
    """ prints expected increase in average survival time between cohorts
    :param cohort_1: first cohort
    :param cohort_2: second cohort
    """

    # increase in proportion of patients who commit suicide
    increase_stat = stats.DifferenceStatIndp(
        x=cohort_2.cohortOutcomes.finalStates,
        y_ref=cohort_1.cohortOutcomes.finalStates
    )

    # mean and confidence interval
    mean = increase_stat.get_mean()
    confidence_int = increase_stat.get_t_CI(alpha=D.ALPHA)

    print("  Expected increase in proportion of patients who commit suicide and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0), mean, confidence_int)
