from MarkovModelClasses import Cohort
from MatrixSupport import MatrixSupport
from SupportComparison import CohortComparison
import MarkovInputData as D
import deampy.in_out_functions as IO

# produce the list to report the results
csv_rows = \
    [['Increase in Access (pp)', 'Suicide Rate', 'Suicide Rate 95% CI', 'Rate Reduction vs. Baseline',
      'Rate Reduction vs. Baseline 95% CI', 'Rate Reduction vs. Previous Scenario',
      'Rate Reduction vs. Previous Scenario 95% CI']]

# create and simulate the baseline cohort
baseline_cohort = Cohort(id=0, pop_size=D.POP_SIZE, transition_prob_matrix=D.TRANS_PROB_MATRIX)
baseline_cohort.simulate()

# add baseline cohort's information to CSV
increase_access = 0
suicide_rate = baseline_cohort.cohortOutcomes.suicideProportion
suicide_rate_CI = baseline_cohort.cohortOutcomes.suicideProportionCI
reduction_from_baseline = 0
reduction_from_baseline_CI = 0
reduction_from_previous = 0
reduction_from_previous_CI = 0
csv_rows.append([increase_access, suicide_rate, suicide_rate_CI, reduction_from_baseline, reduction_from_baseline_CI,
                 reduction_from_previous, reduction_from_previous_CI]
                 )

# create matrix support object
matrix_support = MatrixSupport(D.TRANS_PROB_MATRIX)

# create cohort comparison object to compare cohort outcomes
cohortComparison = CohortComparison()

# set the previous cohort equal to the baseline cohort for the first step of the for loop
previous_cohort = baseline_cohort

# simulate cohorts with increasing levels of access
for i in range(1,4):
    # create matrix with increasing levels of access (4, 8, 12 pp)
    matrix_support.raiseAccess(percentage_points=i*4)

    # simulate a cohort using the matrix
    cohort = Cohort(id=i, pop_size=D.POP_SIZE, transition_prob_matrix=matrix_support.transProbMatrix)
    cohort.simulate()

    # record cohort's increase in access, suicide rate, and suicide rate CI
    increase_access = i*4
    suicide_rate = cohort.cohortOutcomes.suicideProportion
    suicide_rate_CI = cohort.cohortOutcomes.suicideProportionCI

    # record cohort's reduction in suicide rate from baseline with CI
    cohortComparison.compare_outcomes(cohort_1=cohort, cohort_2=baseline_cohort)
    reduction_from_baseline = cohortComparison.rateIncrease
    reduction_from_baseline_CI = cohortComparison.rateIncreaseCI

    # record cohort's reduction in suicide rate from previous cohort with CI
    cohortComparison.compare_outcomes(cohort_1=cohort, cohort_2=previous_cohort)
    reduction_from_previous = cohortComparison.rateIncrease
    reduction_from_previous_CI = cohortComparison.rateIncreaseCI

    # add results to CSV
    csv_rows.append(
        [increase_access, suicide_rate, suicide_rate_CI, reduction_from_baseline, reduction_from_baseline_CI,
         reduction_from_previous, reduction_from_previous_CI]
        )

    # reset matrix to baseline
    matrix_support.raiseAccess(percentage_points=i*-4)

    # set previous cohort to current cohort
    previous_cohort = cohort

# write the results into a csv file
IO.write_csv(file_name='IncreasedAccess.csv', rows=csv_rows)
