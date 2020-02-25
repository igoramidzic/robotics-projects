class PID:
    def __init__(self, kp, cmin, cmax):
        self.KP = kp
        self.Cmin = cmin
        self.Cmax = cmax

    def e(self, desiredDistance, currentDistance):
        return currentDistance - desiredDistance

    def u(self, distanceError):
        return self.KP * distanceError

    def ur(self, desiredVelocity):
        return self.fsat(desiredVelocity)

    def fsat(self, desiredVelocity):
        if desiredVelocity > self.Cmax:
            return self.Cmax
        if self.Cmin <= desiredVelocity <= self.Cmax:
            return desiredVelocity
        return self.Cmin

    def getDesiredSpeed(self, desiredDistance, currentDistance):
        # print("y(t):", -1 * currentDistance)
        distanceError = self.e(desiredDistance, currentDistance)
        # print("e(t):", distanceError)
        ips = self.u(distanceError)
        # print("u(t):", ips)
        saturatedIPS = self.fsat(ips)
        print("ur(t):", saturatedIPS)
        return saturatedIPS
