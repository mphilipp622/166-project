
class QLearn:

    def __init__(self):
        self.rewardDiscount = 0.5
        self.learningRate = 0.2
        self.epsilon = 0.3

        self.qTable = dict()    # will store q values using (state, action) keys and a floating point value
    
    # def 