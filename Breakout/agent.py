import time

class prediction():
    def __init__(self, function):
        self.function    = function
        self.relativePos = (0, 0)
        self.previousPos = (0, 0)
        self.predictPos  = (0, 0)
        self.ballSpeed   = (0, 0)
        self.lastScore   = 0 
        self.lastScoreUpdate = 0
        self.x_Max = 794
        self.x_Min = 0
        self.y_Max = 555
        self.y_Min = 0

    def __call__(self, instr):
        ballPos, paddlePos, paddleWidth, lives, score = extract(instr.decode("utf-8"))
        self.relativePos = (ballPos[0] - paddlePos, ballPos[1])
        newBallSpeed   = (ballPos[0] - self.previousPos[0], ballPos[1] - self.previousPos[1])
        self.previousPos = ballPos

        if newBallSpeed != self.ballSpeed:
            self.ballSpeed  = newBallSpeed
            self.predictPos = self.predictBallLocation()

        if score < 10:
            return self.function(relativePos=self.relativePos)

        if score > self.lastScore:
            self.lastScore = score
            self.lastScoreUpdate = time.time()

        if self.lastScore > 10 and self.lastScoreUpdate > 5 and lives >= 2:
            if paddleWidth <= 30: return 0

        if self.ballSpeed[1] > 0:
            if paddlePos - (paddleWidth // 4) > self.predictPos[0]: 
                return -1
            elif paddlePos + (paddleWidth // 4) < self.predictPos[0]: 
                return 1 
            else: return 0
        
        elif self.ballSpeed[1] < 0:
            return self.function(relativePos=self.relativePos)

    def predictBallLocation(self):
        xGrid, yGrid = 999, 999
        if self.ballSpeed[0] < 0:
            xGrid = (self.previousPos[0] - self.x_Min) // (-self.ballSpeed[0])
        elif self.ballSpeed[0] > 0:
            xGrid = (self.x_Max - self.previousPos[0]) // self.ballSpeed[0]

        if self.ballSpeed[1] < 0:
            yGrid = (self.previousPos[1] - self.y_Min) // (-self.ballSpeed[1])
        elif self.ballSpeed[1] > 0:
            yGrid = (self.y_Max - self.previousPos[1]) // self.ballSpeed[1]

        grid = min(xGrid, yGrid)
        predict_X = self.previousPos[0] + grid * self.ballSpeed[0]
        predict_Y = self.previousPos[1] + grid * self.ballSpeed[1]

        return predict_X, predict_Y

@prediction
def decide(instr = None, **kwargs):
    direction = 0

    if kwargs["relativePos"][0] < 0:
        direction = -1
    elif kwargs["relativePos"][0] > 0:
        direction = 1

    return direction

def extract(instr: str):
    info = instr.split(" ")
    ballPos      = (int(info[0]), int(info[1]))
    paddlePos    = int(info[2])
    paddleWidth  = int(info[3])
    lives        = int(info[4])
    score        = int(info[5])
    # remainBlocks = (len(info) - 6) / 3

    return ballPos, paddlePos, paddleWidth, lives, score