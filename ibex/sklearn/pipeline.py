from __future__ import absolute_import


import operator
import inspect

from sklearn import pipeline as _orig
from sklearn import base
import six
import numpy as np
import pandas as pd

import ibex
from .._base import Pipeline as PDPipeline
from .._base import FeatureUnion as PDFeatureUnion


# Tmp Ami - this should be in a common file
for name in dir(_orig):
    if name.startswith('_'):
        continue
    est = getattr(_orig, name)
    try:
        if inspect.isclass(est) and issubclass(est, base.BaseEstimator):
            globals()[name] = ibex.frame(est)
        else:
            globals()[name] = est
    except TypeError as e:
        pass


def make_pipeline(*estimators):
    """
    Creates a pipeline from estimators.

    Arguments:

        transformers: Iterable of estimators.

    Returns:

        A :class:`ibex.sklearn.pipeline.Pipeline` object.

    Example:

        >>> from ibex.sklearn import preprocessing
        >>> from ibex.sklearn import linear_model
        >>> from ibex.sklearn import pipeline
        >>>
        >>> pipeline.make_pipeline(preprocessing.StandardScaler(), linear_model.LinearRegression())
        Pipeline(...
    """
    estimators = list(estimators)

    if len(estimators) > 1:
        return six.moves.reduce(operator.or_, estimators[1:], estimators[0])

    name = type(estimators[0]).__name__.lower()
    return PDPipeline([(name, estimators[0])])


def make_union(*transformers):
    """
    Creates a union from transformers.

    Arguments:

        transformers: Iterable of transformers.

    Returns:

        A :class:`ibex.sklearn.pipeline.FeatureUnion` object.

    Example:

        >>> from ibex.sklearn import preprocessing as pd_preprocessing
        >>> from ibex.sklearn import pipeline as pd_pipeline

        >>> trn = pd_pipeline.make_union(pd_preprocessing.StandardScaler(), pd_preprocessing.MaxAbsScaler())
    """

    transformers = list(transformers)

    if len(transformers) > 1:
        return six.moves.reduce(operator.add, transformers[1:], transformers[0])

    name = type(transformers[0]).__name__.lower()
    return PDFeatureUnion([(name, transformers[0])])


globals()['Pipeline'] = PDPipeline
globals()['FeatureUnion'] = PDFeatureUnion