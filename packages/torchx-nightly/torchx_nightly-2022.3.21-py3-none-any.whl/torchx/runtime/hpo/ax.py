#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import inspect
from typing import Any, Callable, Dict, Mapping, Optional, Set, cast, Iterable

import pandas as pd
from ax.core import Trial
from ax.core.base_trial import BaseTrial
from ax.core.data import Data
from ax.core.metric import Metric
from ax.core.runner import Runner as ax_Runner
from ax.service.scheduler import TrialStatus
from pyre_extensions import none_throws
from torchx.runner import Runner, get_runner
from torchx.runtime.tracking import FsspecResultTracker
from torchx.specs import AppDef, AppState, AppStatus, CfgVal


_TORCHX_APP_HANDLE: str = "torchx_app_handle"
_TORCHX_RUNNER: str = "torchx_runner"
_TORCHX_TRACKER_BASE: str = "torchx_tracker_base"

# maps torchx AppState to Ax's TrialStatus equivalent
APP_STATE_TO_TRIAL_STATUS: Dict[AppState, TrialStatus] = {
    AppState.UNSUBMITTED: TrialStatus.CANDIDATE,
    AppState.SUBMITTED: TrialStatus.STAGED,
    AppState.PENDING: TrialStatus.STAGED,
    AppState.RUNNING: TrialStatus.RUNNING,
    AppState.SUCCEEDED: TrialStatus.COMPLETED,
    AppState.CANCELLED: TrialStatus.ABANDONED,
    AppState.FAILED: TrialStatus.FAILED,
    AppState.UNKNOWN: TrialStatus.FAILED,
}


class AppMetric(Metric):
    """
    Fetches AppMetric (the observation returned by the trial job/app)
    via the ``torchx.tracking`` module. Assumes that the app used
    the tracker in the following manner:

    .. code-block:: python

     tracker = torchx.runtime.tracking.FsspecResultTracker(tracker_base)
     tracker[str(trial_index)] = {metric_name: value}

     # -- or --
     tracker[str(trial_index)] = {"metric_name/mean": mean_value,
                                 "metric_name/sem": sem_value}

    """

    def fetch_trial_data(self, trial: BaseTrial, **kwargs: Any) -> Data:
        tracker_base = trial.run_metadata[_TORCHX_TRACKER_BASE]
        tracker = FsspecResultTracker(tracker_base)
        res = tracker[trial.index]

        if self.name in res:
            mean = res[self.name]
            sem = None
        else:
            mean = res.get(f"{self.name}/mean")
            sem = res.get(f"{self.name}/sem")

        if mean is None and sem is None:
            raise KeyError(
                f"Observation for `{self.name}` not found in tracker at base `{tracker_base}`."
                f" Ensure that the trial job is writing the results at the same tracker base."
            )

        df_dict = {
            "arm_name": none_throws(cast(Trial, trial).arm).name,
            "trial_index": trial.index,
            "metric_name": self.name,
            "mean": mean,
            "sem": sem,
        }
        return Data(df=pd.DataFrame.from_records([df_dict]))


class TorchXRunner(ax_Runner):
    """
    An implementation of ``ax.core.runner.Runner`` that delegates job submission
    to the TorchX Runner. This runner is coupled with the torchx component
    since Ax runners run trials of a single component with different parameters.

    It is expected that the experiment parameter names and types match
    EXACTLY with component's function args. Component function args that are
    NOT part of the search space can be passed as ``component_const_params``.
    The following args (provided that the component function declares them
    in the function signature) as passed automatically:


    1. ``trial_idx (int)``: current trial's index
    2. ``tracker_base (str)``: torchx tracker's base (typically a URL indicating the base dir of the tracker)

    Example:

    .. code-block:: python

     def trainer_component(
        x1: int,
        x2: float,
        trial_idx: int,
        tracker_base: str,
        x3: float,
        x4: str) -> spec.AppDef:
        # ... implementation omitted for brevity ...
        pass

    The experiment should be set up as:

    .. code-block:: python

     parameters=[
       {
         "name": "x1",
         "value_type": "int",
         # ... other options...
       },
       {
         "name": "x2",
         "value_type": "float",
         # ... other options...
       }
     ]

    And the rest of the arguments can be set as:

    .. code-block:: python

     TorchXRunner(
        tracker_base="s3://foo/bar",
        component=trainer_component,
        # trial_idx and tracker_base args passed automatically
        # if the function signature declares those args
        component_const_params={"x3": 1.2, "x4": "barbaz"})

    Running the experiment as set up above results in each trial running:

    .. code-block:: python

     appdef = trainer_component(
                x1=trial.params["x1"],
                x2=trial.params["x2"],
                trial_idx=trial.index,
                tracker_base="s3://foo/bar",
                x3=1.2,
                x4="barbaz")

     torchx.runner.get_runner().run(appdef, ...)

    """

    def __init__(
        self,
        tracker_base: str,
        component: Callable[..., AppDef],
        component_const_params: Optional[Dict[str, Any]] = None,
        scheduler: str = "local",
        cfg: Optional[Mapping[str, CfgVal]] = None,
    ) -> None:
        self._component: Callable[..., AppDef] = component
        self._scheduler: str = scheduler
        self._cfg: Optional[Mapping[str, CfgVal]] = cfg
        # need to use the same runner in case it has state
        # e.g. torchx's local_scheduler has state hence need to poll status
        # on the same scheduler instance
        self._torchx_runner: Runner = get_runner()
        self._tracker_base = tracker_base
        self._component_const_params: Dict[str, Any] = component_const_params or {}

    def run(self, trial: BaseTrial) -> Dict[str, Any]:
        """
        Submits the trial (which maps to an AppDef) as a job
        onto the scheduler using ``torchx.runner``.

        ..  note:: only supports `Trial` (not `BatchTrial`).
        """

        if not isinstance(trial, Trial):
            raise ValueError(
                f"{type(trial)} is not supported. Check your experiment setup"
            )

        parameters = dict(self._component_const_params)
        parameters.update(none_throws(trial.arm).parameters)
        component_args = inspect.getfullargspec(self._component).args
        if "trial_idx" in component_args:
            parameters["trial_idx"] = trial.index

        if "tracker_base" in component_args:
            parameters["tracker_base"] = self._tracker_base

        appdef = self._component(**parameters)
        app_handle = self._torchx_runner.run(appdef, self._scheduler, self._cfg)
        return {
            _TORCHX_APP_HANDLE: app_handle,
            _TORCHX_RUNNER: self._torchx_runner,
            _TORCHX_TRACKER_BASE: self._tracker_base,
        }

    def poll_trial_status(
        self, trials: Iterable[BaseTrial]
    ) -> Dict[TrialStatus, Set[int]]:
        trial_statuses: Dict[TrialStatus, Set[int]] = {}

        for trial in trials:
            app_handle: str = trial.run_metadata[_TORCHX_APP_HANDLE]
            torchx_runner = trial.run_metadata[_TORCHX_RUNNER]
            app_status: AppStatus = torchx_runner.status(app_handle)
            trial_status = APP_STATE_TO_TRIAL_STATUS[app_status.state]

            indices = trial_statuses.setdefault(trial_status, set())
            indices.add(trial.index)

        return trial_statuses

    def stop(self, trial: BaseTrial, reason: Optional[str] = None) -> Dict[str, Any]:
        """Kill the given trial."""
        app_handle: str = trial.run_metadata[_TORCHX_APP_HANDLE]
        self._torchx_runner.stop(app_handle)
        return {"reason": reason} if reason else {}
