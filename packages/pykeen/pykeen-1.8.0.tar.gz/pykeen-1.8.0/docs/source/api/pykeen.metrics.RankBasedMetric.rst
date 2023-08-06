RankBasedMetric
===============

.. currentmodule:: pykeen.metrics

.. autoclass:: RankBasedMetric
   :show-inheritance:

   .. rubric:: Attributes Summary

   .. autosummary::

      ~RankBasedMetric.binarize
      ~RankBasedMetric.needs_candidates
      ~RankBasedMetric.supported_rank_types

   .. rubric:: Methods Summary

   .. autosummary::

      ~RankBasedMetric.__call__
      ~RankBasedMetric.expected_value
      ~RankBasedMetric.get_sampled_values
      ~RankBasedMetric.numeric_expected_value
      ~RankBasedMetric.numeric_expected_value_with_ci
      ~RankBasedMetric.numeric_variance
      ~RankBasedMetric.numeric_variance_with_ci
      ~RankBasedMetric.std
      ~RankBasedMetric.variance

   .. rubric:: Attributes Documentation

   .. autoattribute:: binarize
   .. autoattribute:: needs_candidates
   .. autoattribute:: supported_rank_types

   .. rubric:: Methods Documentation

   .. automethod:: __call__
   .. automethod:: expected_value
   .. automethod:: get_sampled_values
   .. automethod:: numeric_expected_value
   .. automethod:: numeric_expected_value_with_ci
   .. automethod:: numeric_variance
   .. automethod:: numeric_variance_with_ci
   .. automethod:: std
   .. automethod:: variance
