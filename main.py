"""
Test comment
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from GameLogic import MuehleLogic, Player
from PyQt5.QtCore import *


IMG_BOMB = QImage("./images/bug.png")
IMG_FLAG = QImage("./images/flag.png")
IMG_START = QImage("./images/rocket.png")
IMG_CLOCK = QImage("./images/clock-select.png")
IMG_BLACK = QImage("./images/black.png")
IMG_WHITE = QImage("./images/white.png")

STATUS_READY = 0
STATUS_PLAYING = 1
STATUS_FAILED = 2
STATUS_SUCCESS = 3


class Pos(QWidget):

    clicked = pyqtSignal(int, int)

    def __init__(self, x, y, tile_id, *args, **kwargs):
        super(Pos, self).__init__(*args, **kwargs)

        self.setFixedSize(QSize(50, 50))

        self.tile_id = tile_id
        self.x = x
        self.y = y
        self.player = -1

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

        if self.player == 0:
            p.drawPixmap(r,QPixmap(IMG_WHITE))
        elif self.player == 1:
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

        self.selected_tiles = [-1,-1]

        self.idMap = [[1,0,0,8,0,0,7],
                      [0,9,0,16,0,15,0],
                      [0,0,17,24,23,0,0],
                      [2,10,18,0,22,14,6],
                      [0,0,19,20,21,0,0],
                      [0,11,0,12,0,13,0],
                      [3,0,0,4,0,0,5]]

        self.players = [0, 0]  # both are human

        w = QWidget()
        hb = QHBoxLayout()

        self.mines = QLabel()
        self.mines.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        f = self.mines.font()
        f.setPointSize(24)
        f.setWeight(75)
        self.mines.setFont(f)
        self.clock.setFont(f)


        self.mines.setText("%03d" % 9)
        self.clock.setText("000")

        self.button = QPushButton()
        self.button.setFixedSize(QSize(32, 32))
        self.button.setIconSize(QSize(32, 32))
        self.button.setIcon(QIcon("./images/smiley.png"))
        self.button.setFlat(True)

        self.button.pressed.connect(self.button_pressed)

        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_BOMB))
        l.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        hb.addWidget(l)

        hb.addWidget(self.mines)
        hb.addWidget(self.button)
        hb.addWidget(self.clock)

        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_CLOCK))
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
                w.clicked.connect(self.make_move)
                #w.expandable.connect(self.expand_reveal)
                #w.ohno.connect(self.game_over)
    def make_move(self, x, y):
        selected_tile = self.grid.itemAtPosition(y, x).widget()

        if self.game.status == self.game.STATUS_LAYING:
            # laying phase
            if self.game.players[self.game.activePlayer].phase == Player.PHASE_LAY:
                active_player = self.game.activePlayer
                res = self.game.makeMove(0, selected_tile.tile_id)
                if res != False:
                    selected_tile.player = active_player
                else:
                    return
            # moving phase
            elif self.game.players[self.game.activePlayer].phase == Player.PHASE_MOVE:
                if self.selected_tiles[0] == -1:
                    if selected_tile.player != self.game.activePlayer:
                        return
                    else:
                        self.selected_tiles[0] = selected_tile
                else:
                    if selected_tile.player != -1:
                        return
                    active_player = self.game.activePlayer
                    self.selected_tiles[1] = selected_tile
                    res = self.game.makeMove(self.selected_tiles[0].tile_id, self.selected_tiles[1].tile_id)
                    if res != False:
                        self.selected_tiles[0].player = -1
                        self.selected_tiles[1].player = active_player
                        self.selected_tiles = [-1,-1]
                    else:
                        return
            # Jumping phase
            elif self.game.players[self.game.activePlayer].phase == Player.PHASE_JUMP:
                if self.selected_tiles[0] == -1:
                    self.selected_tiles[0] = selected_tile
                else:
                    self.selected_tiles[1] = selected_tile
                    res = self.game.makeMove(self.selectedTiles[0].tile_id, self.selectedTiles[1].tile_id)
                    if res != False:
                        self.selected_tiles[0].player = -1
                        self.selected_tiles[1].player = self.game.active_player
                        self.selected_tiles = [-1, -1]
                    else:
                        return

        elif self.game.status == self.game.STATUS_MILLDES:
            if self.game.designateKill(selected_tile.tile_id):
                selected_tile.player = -1

        # check possible moves for each player
        # check lose


        self.update()
        self.nextMove()

    def nextMove(self):
        if self.players[self.game.activePlayer] == 1: # its a robot
            print('AI not yet implemented...')
            # if KI --> let KI chose


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()



