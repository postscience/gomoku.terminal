import string
import os
import time
import colors

class Tic:

    SIZE = 15
    ALPHA = string.ascii_lowercase.replace('i', '')
    SYMBOLS = ('X', 'O')
    COLORS = { 'X': colors.BRIGHT_BLUE, 'O': colors.RED, ' ': colors.RESET }
    PATTERNS = (
                ((0,0), (1,0), (2,0), (3,0), (4,0)),
                ((0,0), (1,1), (2,2), (3,3), (4,4)),
                ((0,0), (0,1), (0,2), (0,3), (0,4)),
                ((0,5), (1,4), (2,3), (3,2), (4,1))
               )

    def __init__(self, size = SIZE, patterns = PATTERNS) -> None:
        self.state = []
        self.SIZE = size
        self.PATTERNS = patterns

    def draw(self, pattern = []):
        os.system('cls||clear')
        for i in reversed(range(self.SIZE)):
            print(' '*4 + '----'*self.SIZE)
            print(f'{i + 1:<3}', end='')
            for k in range(self.SIZE):
                field = (i, k)
                symbol = self.SYMBOLS[self.state.index(field) % 2] if field in self.state else ' '
                background = colors.GREEN if field in pattern else ''
                s = '|' + self.COLORS[symbol] + background + f' {symbol} ' + colors.RESET
                print(s, end='')
            print('|')
        print(' '*4 + '----'*self.SIZE)
        print(' '*5, end='')
        for i in range(self.SIZE):
            print(f'{self.ALPHA[i].upper():^4}', end='')
        print('\n')

        
    def move(self, move: str):
        try:
            x, y = int(move[1:]) - 1, self.ALPHA.index(move[0].lower()) 
        except:
            print(f'Well, well, well... Unusual move. You better reconsider..')
            return False
        
        if not x in range(self.SIZE) or not y in range(self.SIZE):
            print(f'Wrong move value: {move}.', 
                  f'Probably typo. Must be in [{self.ALPHA[0:self.SIZE].upper()}] x [1...{self.SIZE}]')
            return False
        
        if (x, y) in self.state:
            print(f'This was already taken: {move}. Try another one')
            return False
        
        return self.update((x, y))
        
    def update(self, move):
        self.state.append(move)
        self.draw()

        player, match = self.has_won()
        if match:
            self.draw(match)
            player_symbol = self.SYMBOLS[player]
            print(f'Stop right here: {player_symbol} just won!!!')
            return True
        
        if len(self.state) == self.SIZE**2:
            print(f'Draw!!! No prizes for you...')
            return True

        return False
    
    def has_won(self):
        n = len(self.state)
        player = (n - 1) % 2
        moves = {self.state[i] for i in range(player, n, 2)}
        last = self.state[-1]
        
        checker = PatternMatcher(moves, self.SIZE - 1)
        for pattern in self.PATTERNS:
            match = checker.match(pattern, last)
            if match:
                break
        return player, match


class PatternMatcher:

    def __init__(self, points: set, border: int) -> None:
        self.space = border
        self.points = points
     
    def translate(self, pattern, vector: tuple[int, int]) -> list:
        return list((x + vector[0], y + vector[1]) for x, y in pattern)
    
    def match(self, pattern, point):
        for s in pattern:
            vector = (point[0] - s[0], point[1] - s[1])
            translated = self.translate(pattern, vector)
            if all(p in self.points for p in translated):
                return translated
        return False


# for tic tac toe 
# patterns for 3x3
patterns3x3 = (
            ((0,0), (1,0), (2,0)),
            ((0,0), (1,1), (2,2)),
            ((0,0), (0,1), (0,2)),
            ((0,2), (1,1), (2,0))
            )
# call Tic(3, patterns3x3)

if __name__ == "__main__":

    tic = Tic()
    tic.draw()

    while True:
        time.sleep(.4)
        move = input('Make a move: ')
        if tic.move(move):
            break

    print("\n\nExited Gomoku.terminal\n")
