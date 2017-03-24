import numpy as np

class StatsRecorder:
    def __init__(self, data=None):
        """
        data: ndarray, shape (nobservations, ndimensions)
        """
        if data is not None:
            self.mean = data.mean(axis=0)
            self.std  = data.std(axis=0)
            self.nobservations = data.shape[0]
        else:
            self.nobservations = 0

    def update(self, data):
        """
        data: ndarray, shape (nobservations, ndimensions)
        """
        if self.nobservations == 0:
            self.__init__(data)
        else:
            newmean = data.mean(axis=0)
            newstd  = data.std(axis=0)

            m = self.nobservations * 1.0
            n = data.shape[0]

            tmp = self.mean

            self.mean = m/(m+n)*tmp + n/(m+n)*newmean
            self.std  = m/(m+n)*(self.std**2 + tmp**2) + \
                        n/(m+n)*(newstd**2 + newmean**2) - self.mean**2
            self.std  = np.sqrt(self.std)

            self.nobservations += n
