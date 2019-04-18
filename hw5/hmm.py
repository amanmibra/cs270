import numpy as np
from hmm_meta import HMM_Meta


class HMM(HMM_Meta):
    """Implementation of the HMM filtering and smoothing algorithms for indoor localization.

    Parameters
    ----------
    width : int
        The width of the building

    length : int
        The length of the building

    rssi_range : int
        The range of signal strength (RSSI) values

    n_beacons : int
        The number of beacons

    sigma : float, optional
        The average step size

    init_pos : a pair of ints, optional
        The initial position (x,y) of the mobile sensor


    Attributes
    ----------
    n_states : int
        The number of states

    rssi_range : int
        The range of signal strength (RSSI) values. The RSSI can take values from 0 to rssi_range-1

    n_beacons : int
        The number of beacons

    init_probs : array, shape(n_states)
        The initial probabilities, P(S_0=i); e.g. self.init_probs[s] stores the probability P(S_0=s)

    trans_probs : array, shape(n_states, n_states)
        The transition matrix (probabilities), P(S_{t+1}=i|S_{t}=j);
        e.g. self.trans_probs[s1,s2] stores the probability P(S_{t+1}=s1|S_{t}=s2)

    obs_probs : array, shape(n,beacons, rssi_range, n_states)
        The array of observation probabilities for each beacon, P(O^{b}_{t}=i|S_{t}=j);
        e.g. self.obs_probs[b,o_b,s] stores the probability P(O^{b}_{t}=o_b|S_{t}=s)


    Examples
    ----------
    Initialization:
    >>> kwargs = {
    ...     'width'     : 32,
    ...     'length'    : 32,
    ...     'rssi_range': 4,
    ...     'n_beacons' : 32,
    ...     'init_pos'  : (0,0)
    ... }
    >>> model = HMM(**kwargs)

    """

    def __init__(self, **kwargs):
        super(HMM, self).__init__(**kwargs)

    def predict(self, probs):
        """Predicts the next state. It computes P(S_{t+1}|O_{1:t}) using probs, which is P(S_{t}|O_{1:t});
        and the transition probabilities P(S_{t+1}|S_{t}).
        Note that none of the probabilities needs to be normalized.

        Parameters
        ----------
        probs : array, shape(n_states)
            The probability vector of the states, which represents P(S_{t}|O_{1:t})

        Returns
        -------
        array, shape(n_states)
            The predicted probabilities, P(S_{t+1}|O_{1:t})

        """
        predicted_probs = np.empty(self.n_states)

        predicted_probs = np.matmul(probs, self.trans_probs)

        # TODO: add your code here
        # Multiply probs with the transition matrix (matrix multiplication) and store the result in predicted_probs
        # You can do that with one line of code using NumPy

        return predicted_probs

    def update(self, probs, o):
        """Updates the probabilities using the observations. It computes probs*P(O_{t}|S_{t}).
        If it is called from the method monitor, then probs represents P(S_{t}|O_{1:t-1})
        and the resulting vector will be proportional to P(S_{t}|O_{1:t}).
        Similarly, if it is called from the method backwards, probs represents P(O_{t+1:T}|S_{t})
        and it will return a vector that is proportional to P(O_{t:T}|S_{t}).

        Parameters
        ----------
        probs : array, shape(n_states)
            The probability vector of the states

        o : array, shape(n_beacons)
            The observation vector, the RSSI values received from each beacon

        Returns
        -------
        array, shape(n_states)
            The updated probabilities, P(S_{t}|O_{1:t}) or P(O_{t:T}|S_{t}) depending on the context

        """
        updated_probs = np.empty(self.n_states)

        # TODO: add your code here
        # Multiply (element-wise) probs with the observation probabilities P(O^{b}_{t}=o[b]|S_{t}) for each beacon b
        # and store the result in updated_probs.

        return updated_probs

    def monitor(self, T, observations):
        """Returns the monitoring probabilities for T time steps using the given sequence of observations.
        In other words, it computes P(S_{t}|O_{1:t}) for each t.
        This procedure is also called filtering, and the algorithm is known as forward algorithm.

        Parameters
        ----------
        T : int
            The number of time steps

        observations: array, shape(T, n_beacons)
            The sequence of observations received

        Returns
        -------
        array, shape(T, n_states)
            The monitoring probabilities, P(S_{t}|O_{1:t}) for each t

        """
        monitoring_probs = np.empty((T, self.n_states))

        # TODO: add your code here
        # Store the initial probabilities in monitoring_probs[0]
        # For t=1,2,...,T-1;
        #     Copy monitoring_probs[t-1] to monitoring_probs[t]
        #     Predict monitoring_probs[t]
        #     Update monitoring_probs[t]
        #     Normalize monitoring_probs[t]

        return monitoring_probs

    def postdict(self, probs):
        """Predicts the previous state. It computes P(O_{t:T}|S_{t-1}) using probs, which is P(O_{t:T}|S_{t});
        and the transition probabilities P(S_{t}|S_{t-1}).
        Note that none of the probabilities needs to be normalized.

        Parameters
        ----------
        probs : array, shape(n_states)
            The probability vector of the states, which represents P(O_{t:T}|S_{t})

        Returns
        -------
        array, shape(n_states)
            The postdicted probabilities, P(O_{t:T}|S_{t-1})

        """
        postdicted_probs = np.empty(self.n_states)
        postdicted_probs[:] = self.trans_probs.T @ probs  # Matrix multiplication
        return postdicted_probs

    def backwards(self, T, observations):
        """Returns the backwards probabilities for T time steps using the sequence of observations.
        In other words, it computes P(O_{t+1:T}|S_{t}) for each t.

        Parameters
        ----------
        T : int
            The number of time steps

        observations: array, shape(T, n_beacons)
            The sequence of observations received

        Returns
        -------
        array, shape(T, n_states)
            The backwards probabilities, P(O_{t+1:T}|S_{t}) for each t

        """
        backwards_probs = np.empty((T, self.n_states))
        backwards_probs[T - 1] = np.ones(self.n_states)
        for t in range(T - 2, -1, -1):
            backwards_probs[t] = backwards_probs[t + 1]
            backwards_probs[t] = self.update(backwards_probs[t], observations[t + 1])
            backwards_probs[t] = self.postdict(backwards_probs[t])
            backwards_probs[t] /= np.sum(backwards_probs[t])  # Normalization
        return backwards_probs

    def hindsight(self, T, observations):
        """Computes the hindsight probabilities by combining the monitoring and backwards probabilities.
        It returns P(S_{t}|O_{1:T}) for each t.

        Parameters
        ----------
        T : int
            The number of time steps

        observations: array, shape(T, n_beacons)
            The sequence of observations received

        Returns
        -------
        array, shape(T, n_states)
            The hindsight probabilities, P(S_{t}|O_{1:T}) for each t

        """
        hindsight_probs = np.empty((T, self.n_states))
        hindsight_probs[:, :] = self.monitor(T, observations) * self.backwards(T, observations)
        hindsight_probs[:, :] = (hindsight_probs.T / np.sum(hindsight_probs, axis=1)).T  # Normalization
        return hindsight_probs
