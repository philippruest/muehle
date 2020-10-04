"""
Test comment
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from GameLogic import MuehleLogic
from PyQt5.QtCore import *

IMG_BOMB = QImage("./images/black.png")
IMG_FLAG = QImage("./images/black.png")
IMG_START = QImage("./images/black.png")
IMG_CLOCK = QImage("./images/black.png")
IMG_BLACK = QImage("./images/black.png")
IMG_WHITE = QImage("./images/white.png")

STATUS_READY = 0
STATUS_PLAYING = 1
STATUS_FAILED = 2
STATUS_SUCCESS = 3

NUM_STONES = 3


class Player:
    PHASE_LAY = 0
    PHASE_MOVE = 1
    PHASE_JUMP = 2
    PHASE_WIN = 3

    ACTION_LMJ = 0
    ACTION_KILL = 1

    COLOR_WHITE = 0
    COLOR_BLACK = 1
    COLOR_NONE = -1

    TYPE_HUMAN = 0
    TYPE_COMPUTER = 1

    def __init__(self, color):
        self.phase = self.PHASE_LAY
        self.action = self.ACTION_LMJ
        self.activeStones = 0
        self.stonesInHand = NUM_STONES
        self.color = color
        self.type = self.TYPE_HUMAN
        self.name = ''
        return


class Pos(QWidget):
    clicked = pyqtSignal(int, int)

    def __init__(self, x, y, tile_id, *args, **kwargs):
        super(Pos, self).__init__(*args, **kwargs)

        self.setFixedSize(QSize(50, 50))

        self.tile_id = tile_id
        self.x = x
        self.y = y
        self.color = Player.COLOR_NONE

    def reset(self):
        self.is_start = False
        self.is_mine = False
        self.adjacent_n = 0

        self.is_revealed = False
        self.is_flagged = False

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        r = event.rect()

        '''
        if self.is_revealed:
            color = self.palette().color(QPalette.Background)
            outer, inner = color, color
        else:
            outer, inner = Qt.gray, Qt.lightGray
        
        
        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_revealed:
            if self.is_start:
                p.drawPixmap(r, QPixmap(IMG_START))

            elif self.is_mine:
                p.drawPixmap(r, QPixmap(IMG_BOMB))

            elif self.adjacent_n > 0:
                pen = QPen(NUM_COLORS[self.adjacent_n])
                p.setPen(pen)
                f = p.font()
                f.setBold(True)
                p.setFont(f)
                p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.adjacent_n))

        elif self.is_flagged:
            p.drawPixmap(r, QPixmap(IMG_FLAG))
        '''
        img_name = './images/id_' + str(self.y) + str(self.x) + '.png'
        p.drawPixmap(r, QPixmap(img_name))

        if self.color == Player.COLOR_WHITE:
            p.drawPixmap(r, QPixmap(IMG_WHITE))
        elif self.color == Player.COLOR_BLACK:
            p.drawPixmap(r, QPixmap(IMG_BLACK))

        ''' 
        # for deubgging
        pen = QPen(QColor('#f44336'))
        p.setPen(pen)
        f = p.font()
        f.setBold(True)
        p.setFont(f)
        p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.tile_id))
        '''

    def flag(self):
        self.is_flagged = True
        self.update()

        self.clicked.emit()

    def unflag(self):
        self.is_flagged = False
        self.update()

        self.clicked.emit()

    def reveal(self):
        self.is_revealed = True
        self.update()

    def click(self):
        '''if not self.is_revealed:
            self.reveal()
            if self.adjacent_n == 0:
                self.expandable.emit(self.x, self.y)

        '''
        if self.tile_id == 0:
            return

        self.clicked.emit(self.x, self.y)

    def mouseReleaseEvent(self, e):
        '''
        # do only input decision here, no logics
        if (e.button() == Qt.RightButton and not self.is_revealed and not self.is_flagged):
            self.flag()

        elif (e.button() == Qt.RightButton and self.is_flagged):
            self.unflag()

        elif (e.button() == Qt.LeftButton):
            self.click()

            if self.is_mine:
                self.ohno.emit()
        '''

        self.click()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.selected_tiles = [-1, -1]

        self.idMap = [[1, 0, 0, 8, 0, 0, 7],
                      [0, 9, 0, 16, 0, 15, 0],
                      [0, 0, 17, 24, 23, 0, 0],
                      [2, 10, 18, 0, 22, 14, 6],
                      [0, 0, 19, 20, 21, 0, 0],
                      [0, 11, 0, 12, 0, 13, 0],
                      [3, 0, 0, 4, 0, 0, 5]]

        self.players = [Player(Player.COLOR_WHITE), Player(Player.COLOR_BLACK)]
        self.players[0].name = 'wPhilipp'
        self.players[1].name = 'bAnnika'

        w = QWidget()
        hb = QHBoxLayout()

        self.whiteStatus = QLabel()
        self.whiteStatus.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.blackStatus = QLabel()
        self.blackStatus.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        f = self.whiteStatus.font()
        f.setPointSize(12)
        f.setWeight(75)
        self.whiteStatus.setFont(f)
        self.blackStatus.setFont(f)

        self.whiteStatus.setText(self.players[0].name)
        self.blackStatus.setText(self.players[1].name)

        self.button = QPushButton()
        self.button.setFixedSize(QSize(32, 32))
        self.button.setIconSize(QSize(32, 32))
        self.button.setIcon(QIcon("./images/black.png"))
        self.button.setFlat(True)

        self.button.pressed.connect(self.button_pressed)

        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_WHITE))
        l.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        hb.addWidget(l)

        hb.addWidget(self.whiteStatus)
        hb.addWidget(self.button)
        hb.addWidget(self.blackStatus)

        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_BLACK))
        l.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hb.addWidget(l)

        vb = QVBoxLayout()
        vb.addLayout(hb)

        self.grid = QGridLayout()
        self.grid.setSpacing(0)

        vb.addLayout(self.grid)
        w.setLayout(vb)
        self.setCentralWidget(w)
        self.init_map()

        self.game = MuehleLogic()
        self.activePlayer = self.players[0]
        self.show()

    def button_pressed(self):
        if self.status == STATUS_PLAYING:
            self.update_status(STATUS_FAILED)
            self.reveal_map()

        elif self.status == STATUS_FAILED:
            self.update_status(STATUS_READY)
            self.reset_map()

    def init_map(self):
        # Add positions to the map
        for x in range(0, 7):
            for y in range(0, 7):
                w = Pos(x, y, self.idMap[y][x])
                self.grid.addWidget(w, y, x)
                # Connect signal to handle expansion.
                w.clicked.connect(self.tile_clicked)
                # w.expandable.connect(self.expand_reveal)
                # w.ohno.connect(self.game_over)

    def tile_clicked(self, x, y):
        selected_tile = self.grid.itemAtPosition(y, x).widget()

        if self.activePlayer.action == Player.ACTION_LMJ:
            # laying phase
            if self.activePlayer.phase == Player.PHASE_LAY:
                active_player = self.activePlayer
                res = self.check_move(0, selected_tile.tile_id)
                if res != False:
                    selected_tile.color = active_player.color
                else:
                    return
            # moving phase
            elif self.activePlayer.phase == Player.PHASE_MOVE:
                if self.selected_tiles[0] == -1:
                    if selected_tile.color != self.activePlayer.color:
                        return
                    else:
                        self.selected_tiles[0] = selected_tile
                else:
                    if selected_tile.color != -1:
                        return
                    active_player = self.activePlayer
                    self.selected_tiles[1] = selected_tile
                    res = self.check_move(self.selected_tiles[0].tile_id, self.selected_tiles[1].tile_id)
                    if res != False:
                        self.selected_tiles[0].color = Player.COLOR_NONE
                        self.selected_tiles[1].color = active_player.color
                        self.selected_tiles = [-1, -1]
                    else:
                        return
            # Jumping phase
            elif self.activePlayer.phase == Player.PHASE_JUMP:
                if self.selected_tiles[0] == -1:
                    self.selected_tiles[0] = selected_tile
                else:
                    self.selected_tiles[1] = selected_tile
                    res = self.check_move(self.selectedTiles[0].tile_id, self.selectedTiles[1].tile_id)
                    if res != False:
                        self.selected_tiles[0].color = -1
                        self.selected_tiles[1].color = self.activePlayer.color
                        self.selected_tiles = [-1, -1]
                    else:
                        return
        elif self.activePlayer.action == Player.ACTION_KILL:
            if self.designate_kill(selected_tile.tile_id):
                selected_tile.color = Player.COLOR_NONE
                self.activePlayer.phase = Player.ACTION_LMJ
                self.switch_player()


        # check lose
        self.check_lose()

        # check possible moves for each player

        self.update()

    def check_move(self, oldField, newField):
        # check if move is allowed
        if oldField == newField:
            print("Using the same field is not allowed")
            return False

        if self.activePlayer.phase == Player.PHASE_LAY:
            if self.game.board[newField] >= 0:
                print("Place already occupied")
                return False
            else:
                self.game.board[newField] = self.activePlayer.color
                self.activePlayer.activeStones += 1
                self.activePlayer.stonesInHand -= 1
                if self.activePlayer.stonesInHand == 0:
                    self.activePlayer.phase = Player.PHASE_MOVE
                if self.check_mill(newField):
                    self.activePlayer.action = Player.ACTION_KILL
                else:
                    self.switch_player()
                return oldField, newField
        elif self.activePlayer.phase == Player.PHASE_MOVE:
            if newField not in self.game.neighbours[oldField]:
                print("Not neighbours")
                return False
            if self.game.board[newField] >= 0:
                print("Place already occupied")
                return
            self.game.board[oldField] = -1
            self.game.board[newField] = self.activePlayer.color
            if self.check_mill(newField):
                self.activePlayer.action = Player.ACTION_KILL
            else:
                self.switch_player()
            return oldField, newField
        elif self.activePlayer.phase == Player.PHASE_JUMP:
            print('implement')

        return

    def check_mill(self, field):
        if self.activePlayer.activeStones < 3:
            return False
        for i in range(len(self.game.millPatterns)):
            if field in self.game.millPatterns[i]:
                print(self.game.millPatterns[i])
                found = True
                for j in range(3):
                    if self.game.board[self.game.millPatterns[i][j]] != self.activePlayer.color:
                        found = False
                if found:
                    print('Found mill')
                    return True
        return False

    def switch_player(self):
        if self.activePlayer == self.players[0]:
            self.activePlayer = self.players[1]
            self.button.setIcon(QIcon("./images/black.png"))
        else:
            self.activePlayer = self.players[0]
            self.button.setIcon(QIcon("./images/white.png"))



    def designate_kill(self, field):
        if self.game.board[field] == self.activePlayer:
            print('Dont kill yourself :-)')
            return False
        if self.game.board[field] == -1:
            print('This field is empty :-)')
            return False

        self.game.board[field] = -1
        self.activePlayer.action = Player.ACTION_LMJ
        self.switch_player()
        self.activePlayer.activeStones -= 1
        return True

    def check_lose(self):
        for player in self.players:
            # check if the player has >= 3 stones avaialable
            if player.stonesInHand + player.activeStones < 3:
                print('Player ' + str(player.color) + ' loses!')
                return True

        # check if players can still make a move
        if not self.check_player_free(0):
            print('Player 0 loses')
        if not self.check_player_free(1):
            print('Player 1 loses')

    def check_player_free(self, player):
        player_free = False
        for i in range(1, len(self.game.board)):
            if self.game.board[i] == player:
                stone_free = False
                for j in range(len(self.game.neighbours[i])):
                    if self.game.board[self.game.neighbours[i][j]] == -1:
                        stone_free = True
                if stone_free:
                    player_free = True
                    break
        return player_free


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()
