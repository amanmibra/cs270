"""Helper code including an abstract HMM class with some plotting functions.
"""
# NOTE: Do not modify this file!

from abc import ABC, abstractmethod
import numpy as np
from itertools import product
import matplotlib.pyplot as plt
from ipywidgets.widgets import IntSlider
from ipywidgets import interact


class HMM_Meta(ABC):
    """Hidden Markov Model class that constructs the transition and the observation models for indoor positioning.

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

    """

    def __init__(self, width, length, rssi_range, n_beacons, sigma=None, init_pos=None):
        self.width = width
        self.length = length
        self.n_states = width * length  # Number of states

        self.rssi_range = rssi_range
        self.n_beacons = n_beacons

        self.sigma = sigma if sigma else np.sqrt(self.n_states) / 16

        self.init_probs = self.get_init_probs(init_pos)
        self.trans_probs = self.get_trans_probs()
        self.obs_probs = np.empty((n_beacons, rssi_range, self.n_states))
        for b in range(n_beacons):
            self.obs_probs[b] = self.get_obs_probs()

    def get_init_probs(self, init_pos=False):
        """Returns the initial probabilities, P(S_0).
        If the initial position is provided, this will return a probability distribution concentrated at that position;
        otherwise it will return a uniform distribution.

        Parameters
        ----------
        init_pos : pair of ints, optional
            The initial position of the mobile sensor

        Returns
        -------
        array, shape(n_states)
            The initial probabilities. The probability P(S_0=i)

        """
        init_probs = np.ones(self.n_states)
        if init_pos:
            s = init_pos[0] + self.width * init_pos[1]
            init_probs[s] = 100 * self.n_states
        init_probs /= np.sum(init_probs)
        return init_probs

    def get_trans_probs(self):
        """Returns the transition probabilities, P(S_{t+1}|S_{t}), a random walk with discretized Gaussian steps.

        Returns
        -------
        array, shape(n_states, n_states)
            The transition matrix. The probability P(S_{t+1}=i|S_{t}=j)

        """
        two_var = 2 * self.sigma * self.sigma
        trans_probs = np.zeros((self.n_states, self.n_states), dtype=np.double)

        for s_x, s_y in product(range(self.width), range(self.length)):  # From the source s
            s = s_y * self.width + s_x
            for t_x, t_y in product(range(self.width), range(self.length)):  # To the target t
                t = t_y * self.width + t_x
                x_dist = t_x - s_x
                y_dist = t_y - s_y
                trans_probs[t, s] = -(x_dist * x_dist + y_dist * y_dist) / two_var  # Log prob

        trans_probs = np.exp(trans_probs)  # Convert log probs to probs
        trans_probs /= np.sum(trans_probs, axis=0)  # Normalize
        return trans_probs

    def get_obs_probs(self):
        """Returns the observation probabilities for a beacon, P(O_{t}|S_{t}).

        Returns
        -------
        array, shape(rssi_range, n_states)
            The observation probabilities. The probability P(O_{t}=i|S_{t}=j)

        """
        obs_probs = np.zeros((self.rssi_range, self.n_states))  # Random probs
        for o in range(self.rssi_range):
            obs_probs[o][np.random.choice(self.n_states, 16)] = 1
            for k in range(2):
                obs_probs[o] = self.trans_probs @ obs_probs[o]
        obs_probs /= np.sum(obs_probs, axis=0)  # Normalize
        return obs_probs

    def generate_path(self, T):
        """Returns a trajectory with the observations received along the path
        using the initial and the transition probabilities.

        Parameters
        ----------
        T : int
            The number of time steps

        Returns
        -------
        a pair of arrays, shape(T) and shape(T, n_beacons)
            The pair of the trajectory, a sequence of states,
            and observations, a vector of RSSI values for each time step

        """
        actual_path = np.empty(T, dtype=np.int)
        actual_path[0] = np.random.choice(self.n_states, p=self.init_probs)
        observations = np.empty((T, self.n_beacons), dtype=np.int)
        for t in range(1, T):
            actual_path[t] = np.random.choice(self.n_states, p=self.trans_probs[:, actual_path[t - 1]])
            for b in range(self.n_beacons):
                observations[t, b] = np.random.choice(self.rssi_range, p=self.obs_probs[b, :, actual_path[t]])

        return actual_path, observations

    def plot_obs_probs(self, b):
        """Plots the heatmap of the observation probabilities of the given beacon b.
        
        Parameters
        ----------
        b : int
            The id of the beacon
            
        """
        obs_probs_reshaped = np.zeros((self.rssi_range, self.width, self.length))
        for o in range(self.rssi_range):
            obs_probs_reshaped[o] = self.obs_probs[b, o].reshape((self.length, self.width))
        xs = np.arange(self.width)
        ys = np.arange(self.length)

        def plot(o):
            """Plots the heatmap of the probabilities of observing the signal strength o.

            Parameters
            ----------
            o : int
                The signal strength

            """
            plt.figure(figsize=(8, 7))
            plt.pcolormesh(xs, ys, obs_probs_reshaped[o], cmap='YlGnBu', vmin=0, vmax=1)
            plt.colorbar(label='Probability')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('$P(O^{(' + str(b) + ')}_t=' + str(o) + '|S_t)$')

        w = IntSlider(value=0, min=0, max=self.rssi_range - 1)

        interact(plot, o=w)

    def plot(self, probs=None, path=None, title=None):
        """Plots the heatmap of the given probabilities (or a list of probabilities) with the path if it is specified.
        
        Parameters
        ----------
        probs : array, shape(n_states), optional
            A probability vector of the states. If it is None, then path must be provided.

        path : array, shape(T), optional
            A sequence of states. If it is None, then probs must be provided.

        title : str, optional
            Either of 'prediction', 'monitoring', or 'hindsight'. It will be used to determine the title of the plot.

        """
        if path is not None:
            T = len(path)
            path_2d = [(s % self.width, s // self.width) for s in path]

        if probs is None:
            probs_reshaped = np.zeros((T, self.width, self.length))
        else:
            probs = [probs] if not isinstance(probs, list) and len(probs.shape) == 1 else probs
            probs = np.array(probs)
            T = probs.shape[0]

            probs_reshaped = np.zeros((T, self.width, self.length))
            for t in range(T):
                probs_reshaped[t] = probs[t].reshape((self.length, self.width))

        xs = np.arange(self.width)
        ys = np.arange(self.length)

        def plot(t):
            """Plots the heatmap of the grid of probabilities at time t.

            Parameters
            ----------
            t : int
                The time step

            """
            plt.figure(figsize=(8, 7))
            plt.pcolormesh(xs, ys, probs_reshaped[t], cmap='YlGnBu', vmin=0, vmax=0.01)
            plt.colorbar(label='Probability')
            plt.xlabel('x')
            plt.ylabel('y')
            if probs is not None:
                if title == 'prediction':
                    plt.title('Prediction: $P(S_{' + str(t) + '})$')
                elif title == 'monitoring':
                    if t == 0:
                        prob_text = 'S_0'
                    elif t == 1:
                        prob_text = 'S_1|O_1'
                    else:
                        prob_text = 'S_{' + str(t) + '}|O_{1:' + str(t) + '}'
                    plt.title('Monitoring: $P(' + prob_text + ')$')
                elif title == 'hindsight':
                    plt.title('Hindsight: $P(S_{' + str(t) + '}|O_{1:' + str(T) + '})$')

            if path is not None:
                t_min = max(t - 8, 0)
                plt.plot([path_2d[t_min][0], path_2d[t_min][0]], [path_2d[t_min][1], path_2d[t_min][1]],
                         'r*', label='Actual Path')
                for tt in range(t_min + 1, t + 1):
                    plt.plot([path_2d[tt - 1][0], path_2d[tt][0]], [path_2d[tt - 1][1], path_2d[tt][1]], '-*',
                             color='orange')
                plt.plot(path_2d[t][0], path_2d[t][1], 'o', color='red',
                         markersize=12, markeredgewidth=1.5, markeredgecolor='green')
                plt.legend()

        w = IntSlider(value=0, min=0, max=T - 1)
        interact(plot, t=w)

        @abstractmethod
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
            pass

        @abstractmethod
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
                The observation vector, RSSI values received from each beacon

            Returns
            -------
            array, shape(n_states)
                The updated probabilities, P(S_{t}|O_{1:t}) or P(O_{t:T}|S_{t}) depending on the context

            """
            pass

        @abstractmethod
        def monitor(self, T, observations):
            """Returns the monitoring probabilities for T time steps using the sequence of observations.
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
            pass

        @abstractmethod
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
            pass

        @abstractmethod
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
            pass

        @abstractmethod
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
            pass
