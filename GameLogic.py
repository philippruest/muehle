

class Player():

    PHASE_LAY = 0
    PHASE_MOVE = 1
    PHASE_JUMP = 2
    PHASE_WIN = 3

    def __init__(self):

        self.phase = 0
        self.activeStones = 0
        return

class MuehleLogic():
    STATUS_LAYING = 0
    STATUS_MILLDES = 1

    NUM_STONES = 3

    neighbours = [[],
                  [2,8],#1
                  [1,10,3],#2
                  [2,4],
                  [3,5,12], #4
                  [4,6],
                  [5,7,14],#6
                  [6,8],
                  [7,1,16],#8
                  [10,16],
                  [9,2,11,18],#10
                  [10,12],
                  [11,4,13,20],#12
                  [12,14],
                  [13,6,15,22],#14
                  [14,16],
                  [15,8,9,24],#16
                  [24,18],
                  [17,10,19],#18
                  [18,20],
                  [19,12,21],#20
                  [20,22],
                  [21,14,23],#22
                  [22,24],
                  [23,16,17]]

    millPatterns = [[1,2,3],
                    [3,4,5],
                    [5,6,7],
                    [7,8,1],
                    [9,10,11],
                    [11,12,13],
                    [13,14,15],
                    [15,16,9],
                    [17,18,19],
                    [19,20,21],
                    [21,22,23],
                    [23,24,17],
                    [2,10,18],
                    [4,12,20],
                    [6,14,22],
                    [8,16,24]]
    def __init__(self):
        self.players =[Player(), Player()]

        self.activePlayer = 0
        self.status = self.STATUS_LAYING

        self.board = [-2, -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

    def makeMove(self,oldField, newField):
        if self.status == self.STATUS_LAYING:
            # check if move is allowed
            if oldField == newField:
                print("Using the same field is not allowed")
                return False

            if self.players[self.activePlayer].phase == Player.PHASE_LAY:
                if self.board[newField] >= 0:
                    print("Place already occupied")
                    return False
                else:
                    self.board[newField] = self.activePlayer
                    self.players[self.activePlayer].activeStones += 1
                    if self.players[self.activePlayer].activeStones == self.NUM_STONES:
                        self.players[self.activePlayer].phase = Player.PHASE_MOVE
                    if self.checkMill(newField):
                        self.status = self.STATUS_MILLDES
                    else:
                        if self.activePlayer == 0:
                            self.activePlayer = 1
                        else:
                            self.activePlayer = 0
                    return oldField, newField
            elif self.players[self.activePlayer].phase == Player.PHASE_MOVE:
                if not newField in self.neighbours[oldField]:
                    print("Not neighbours")
                    return False
                if self.board[newField] >= 0:
                    print("Place already occupied")
                    return
                self.board[oldField] = -1
                self.board[newField] = self.activePlayer
                if self.checkMill(newField):
                    self.status = self.STATUS_MILLDES
                else:
                   self.switchActivePlayer()
                return oldField, newField
            elif self.phase == Player.PHASE_JUMP:
                 print('implement')

        return

    def designateKill(self,field):
        if self.board[field] == self.activePlayer:
            print('Dont kill yourself :-)')
            return False
        if self.board[field] == -1:
            print('This field is empty :-)')
            return False

        self.board[field] = -1
        self.status = self.STATUS_LAYING
        self.switchActivePlayer()
        self.players[self.activePlayer].activeStones -= 1
        return True

    def checkMill(self,field):
        if self.players[self.activePlayer].activeStones<3:
            return False
        for i in range(len(self.millPatterns)):
            if field in self.millPatterns[i]:
                print(self.millPatterns[i])
                found = True
                for j in range(3):
                    if self.board[self.millPatterns[i][j]] != self.activePlayer:
                        found = False
                if found: break
        return found

    def switchActivePlayer(self):
        if self.activePlayer == 0:
            self.activePlayer = 1
        else:
            self.activePlayer = 0
