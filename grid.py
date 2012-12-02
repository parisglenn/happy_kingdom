import random
import copy

class bcolors:
    PURPLE = '\033[35m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PINK = '\033[95m'
    TEAL = '\033[96m'
    GRAY = '\033[97m'
    BLACK = '\033[98m'
    ENDC = '\033[0m'

class Grid(object):

    def __init__(self, width=30, height=30, verbose=False, distro={1:160,2:40,3:20}, above_bias=40, diag_bias=42, side_bias=30, repeat_decrease=3, print_color=True, reduce_one=True):
        '''A higher repeate decrease will mean that a 2s and 3s will be less likely to appear within a context of all 1s '''
        self.width = width
        self.height = height
        self.verbose = verbose
        self.color = print_color
        self.final_grid = []
        self.default_distro = copy.deepcopy(distro)
        self.above_bias = above_bias
        self.diag_bias = diag_bias
        self.side_bias = side_bias
        self.reduce_one = reduce_one
        self.repeat_decrease = repeat_decrease
        self.colors = {1:bcolors.GREEN, 2:bcolors.YELLOW, 3:bcolors.BLUE}
        self._create_frame()
        self.create_grid(verbose)

    def _create_frame(self):
        for i in range(self.height):
            self.final_grid.append([])
       
    def create_grid(self, verbose):
        for i in range(self.height):
            row = self.final_grid[i]
            for k in range(self.width):
                k = self._choose_cell(i,k)
                row.append(k) 
        if self.verbose:
            print self
        if self.color:
            self._print_color()   

    def _print_color(self):
        for row in self.final_grid:
            for i in row:
                hue = self.colors[i]
                formated = hue + u"\u2588" + bcolors.ENDC
                print formated,
            print   

    def __str__(self):
        string_grid = ''
        for row in self.final_grid:
            for i in row:
                hue = self.colors[i]
                string_grid += hue + ''.join("# ") + bcolors.ENDC
            string_grid += ('\n')
        return string_grid

    def _choose_cell(self, i, k):
        if i == 0:
            cell = random.choice(self.distro_to_list(self.default_distro))
        else: #find what was is around the cell being created
            previous_row = self.final_grid[i-1]
            current_row = self.final_grid[i]
            above = previous_row[k]
            if k > 0:
                upper_left = previous_row[k-1]
                side = current_row[k-1]
            else:
                upper_left = None
                side = None
            if k < self.width-1:
                upper_right = previous_row[k+1] 
            else:
                upper_right = None
            possibles = self._create_distro(upper_left, above, upper_right, side)
            cell = random.choice(possibles)
            #reduce the chance or a river or mountain originating each time one has already initiated
            if cell != 1 and upper_left != cell and above != cell and upper_right != cell and self.default_distro[cell] >= 0:
                self._reduce_distro(cell)
        return cell    

    def _create_distro(self, upper_left, above, upper_right, side):
        distro = copy.deepcopy(self.default_distro)
        distro = self._adjust_distro('above', above, distro)
        if upper_left:
            distro = self._adjust_distro('upper_left', upper_left, distro)
        if upper_right:
            distro = self._adjust_distro('upper_right', upper_right, distro)            
        if side:
            distro = self._adjust_distro('side', side, distro)            
        possibles = self.distro_to_list(distro)
        return possibles

    def _adjust_distro(self, position, value, distro):
        biases = {'upper_left':self.diag_bias, 'upper_right':self.diag_bias, 'above':self.above_bias, 'side':self.side_bias}
        bias = biases[position]
        position_index = distro.get(value,0)
        position_index += bias
        distro[value] = position_index
        if self.reduce_one:
            one_index = distro[1]
            one_index -= bias
            distro[1] = one_index
        return distro

    def _reduce_distro(self, key):
        val = self.default_distro[key]
        new_val = val - self.repeat_decrease
        self.default_distro[key] = new_val
        
    def distro_to_list(self, seq):
        possibles = []
        for key in seq:
            freq = seq.get(key, 0)
            for i in range(freq):
                possibles.append(key)       
        return possibles
        
class Cell():

    def __init__():
        elevation = 1
        minerals = 1
        flora = 1
        fauna = 1

class Grass(Cell):

    def __init__():
        pass
