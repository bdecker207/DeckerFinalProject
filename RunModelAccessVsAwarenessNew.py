from MarkovModelClasses import Cohort
from MatrixSupport import MatrixSupport
from SupportComparison import CohortComparison
import MarkovInputData as D
import deampy.in_out_functions as IO

# produce the list to report the results
csv_rows = \
    [['Percentage Point Increase', 'Suicide Rate Awareness', 'Suicide Rate Access', 'Rate Reduction Access',
      '95% CI Rate Reduction Access']]

# create matrix support object
matrix_support = MatrixSupport(D.TRANS_PROB_MATRIX_2)

# create cohort comparison object to compare cohort outcomes
cohortComparison = CohortComparison()

# simulate cohorts with increasing levels of awareness and access
for i in range(1,3):
    # create matrix with increasing levels of awareness (4, 8, 12 pp)
    matrix_support.raiseAwareness(percentage_points=i*4)

    # simulate a cohort using the matrix (set IDs to so they match the IDs from other increased awareness exercise)
    cohort_awareness = Cohort(id=i+3, pop_size=D.POP_SIZE, transition_prob_matrix=matrix_support.transProbMatrix)
    cohort_awareness.simulate()

    # record cohort's suicide rate
    suicide_rate_awareness = cohort_awareness.cohortOutcomes.suicideProportion

    # reset awareness level and raise access level
    matrix_support.raiseAwareness(percentage_points=i * -4)
    matrix_support.raiseAccess(percentage_points=i * 4)

    # simulate a cohort using the matrix (set IDs so they match the IDs from other increased access exercise)
    cohort_access = Cohort(id=i, pop_size=D.POP_SIZE, transition_prob_matrix=matrix_support.transProbMatrix)
    cohort_access.simulate()

    # record cohort's suicide rate
    suicide_rate_access = cohort_access.cohortOutcomes.suicideProportion

    # record reduction in suicide rate if increase access instead of awareness; record 95% CI
    cohortComparison.compare_outcomes(cohort_1=cohort_access, cohort_2=cohort_awareness)
    rate_reduction = cohortComparison.rateIncrease
    rate_reduction_CI = cohortComparison.rateIncreaseCI

    # add results to CSV
    csv_rows.append(
        [i*4, suicide_rate_awareness, suicide_rate_access, rate_reduction, rate_reduction_CI]
        )

    # reset matrix to baseline
    matrix_support.raiseAccess(percentage_points=i*-4)

# write the results into a csv file
IO.write_csv(file_name='AccessVsAwarenessNew.csv', rows=csv_rows)