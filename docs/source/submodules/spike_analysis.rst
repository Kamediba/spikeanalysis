SpikeAnalysis
=============

The :code:`SpikeAnalysis` is the major analysis class. It uses :code:`events` and the :code:`spike_times` in order to calculate common spike train metrics,
e.g., PSTH (peristimulus histograms), z-scored data, latency to first spike, trial-trial correlations.

Setting Stimulus and Spike Data
-------------------------------

:code:`SpikeAnalysis` requires both :code:`StimulusData` and :code:`SpikeData` to perform analyses. It has a setting method for each of these datasets.

.. code-block:: python

    # stim = StimulusData
    # spikes = SpikeData

    from spikeanalysis.spike_analysis import SpikeAnalysis

    spiketrain = SpikeAnalysis()
    spiketrain.set_stimulus_data(event_times = stim)
    spiketrain.set_spike_data(sp = spikes)

Calculating Peristimulus Histogram (PSTH)
-----------------------------------------

The PSTH seeks to align spike times for each unit to stimulus timing for various stimuli.
Under the hood this just uses :code:`np.histogram` in order to count spikes for the given
values. Of note this is based on :code:`samples` rather than :code:`time` which allows the 
counts to occur over :code:`ints` rather than over :code:`floats`, which reduces potential
rounding errors. In order to calculate the PSTH the :code:`time_bin_ms` must be loaded, which
is the time in milliseconds to be converted into :code:`samples` under the hood. The :code:`window`
must also be given. Ideally this window should include time before and after the events. For example
a :code:`window=[-10, 20]` would be 10 seconds before each stimulus to 20 seconds after each stimulus.
The window can always be shrunk for plotting functions, but keeping a wide, but non-overlapping
window can demonstrate some patterns that might be missed by only focusing on right around the stimulus
onset. Also traditionally PSTHs should only have 0 or 1 spikes/bin and so the code will indicate
if your current time_bin_ms is too large to fulfil this condition. It is up to the user whether this
matters for their purposes. Additionally this function can globally apply values or each stimulus can have
a value given.

.. code-block:: python

    spiketrain.get_raw_psth(time_bin_ms=0.01, window=[-10,20]) # same values used

or

.. code-block:: python

    spiketrain.get_raw_psth(time_bin_ms=1, window=[[-10,20], [-.5, 1]]) # different windows

Z-scoring Data
--------------

Neuron firing rates can be z-scored to assess change in firing rate between baseline periods and stimulus periods.
It is often beneficial to change the :code:`time_bin` for Z scoring to smoothing the data. (1 and 0s lead to very noisy z scores)
Increasing bin size will allow the large time bins to have a more continuous distribution of spike counts. In order to use this 
function a :code:`bsl_window` should be given. This should be the pre-stimulus baseline of the neuron/unit. The window is then the window
over which to Z score. It is beneficial to still include the before and after stimulus windows to better see how the z score has
changed. Simimlarly each stimulus can have its own window by doing nested lists. The math is relatively standard:

.. math::

    Z = \frac{x - \mu}{\sigma}

    Z_{avg} = \frac{1}{N_{trials}} \Sigma^{N_{trials}} Z

In our example below we determine both our :math:`\mu` and our :math:`\sigma` with the :code:`bsl_window` and 
then z score each time bin given by :code:`time_bin_ms` over the :code:`window`

.. code-block:: python
    
    spiketrain.z_score_data(time_bin_ms = 50, bsl_window=[-10,0], z_window=[-10,20])


Latency to first spike
----------------------

Another assessment of a neuron is the latency to fire after stimulus onset. Different populations require different mathematical models
For neurons which follow a Poisson distribution a statistical test checking for the first deviation from this distribution can be used. 
For neurons that are relatively quiescent, time to the first spike is more accurate. :code:`SpikeAnalysis` currently uses a cutoff of 2Hz
baseline firing to determine which measurement to make for determining latency to fire (cutoff as suggested by Mormann et al 2008). 
The desired baseline window should be given, the :code:`time_bin_ms` allows for the calculation of the deviation from a Poisson (see note below) 
and the :code:`num_shuffles` indicates how many baseline shuffles to store.

.. code-block:: python

    spiketrain.latencies(bsl_window = [-30,-10], time_bin_ms = 50.0, num_shuffles = 300)


Above 2Hz Assuming a Poisson
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adapted from Chase and Young **PNAS** 2007 the neurons firing rate is assumed to follow a Poisson distribution with a PMF of:

.. math:: 

    f(x) = \frac{\mu e^{-\mu}}{k!}

To calculate the potential deviation from this distribution we perform a calculation based on the CDF:

.. math::

    P_{t_n}(\geq n) = 1 - \sum_{m=0}^{n-1} \frac{( \lambda t_n)^m e^{- \lambda t_n}}{m!}

In this case the :math:`\lambda` is the baseline firing rate of the neuron and :math:`t_n` will be the time window. They calcuate to see
first latency to spike based on all trials being merged, but in :code:`spikeanalysis` each trial is taken separately so that a distribution
can be determined of the latencies rather than just one value. The take a threshold of :math:`10^{-6}`, which is maintained, but may be
changed in the future.

Note :math:`\lambda` * :math:`t_n` gives us the :math:`\mu` from the standard Poisson PMF.

Below 2Hz Taking the first-spike
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the mean firing rate is below 2Hz for a neuron, the first spike is taken to be the true first spike as related to the stimulus. This 
means that the neuron is not following a Poisson distribution and so taking the first spike time is likely acceptable see Emmanuel et al. 2021
for use of this technique in DRG neurons and Mornmann et al. 2008 for use in human cortex.



Shuffled baseline
^^^^^^^^^^^^^^^^^

To allow for statistical tests to assess changes in latency to fire for a unit, a shuffled baseline is created at the same time. This is just
based on a normal distribution of points before the onset of the stimulus. By shuffling the baseline we can assess whether the true latency to fire
is truly distinct.


Interspike Interval
-------------------

Interspike intervals are the times between a neuron firing. The limit of this is the refractory period, ie, the time at which a neuron can not
fire even if maximally stimulated. The distribution of these intervals can provide information about the neurons firing rate distribution
as well Gaussian vs Poisson ISI distributions having distinct PSTHs.


Autocorrelogram
---------------

Calculating an Autocorrelogram for each unit based on its spike times. The 0 lag sample is removed. This is returned as a :code:`np.ndarray` for ease of use.
Currently it is based on bins with size :math:`\frac{1}{2} SampleSize`, but this may evenutually become an argument in the function.

.. code-block:: python

    spiketrain.autocorrelogram()



References
----------

TODO
