#from termcolor import colored
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

    def __init__(self, width=14, height=14, verbose=False, distro={1:150,2:40,3:20}, above_bias=60, diag_bias=40, side_bias=40, repeat_decrease=8, color=True):
        '''A higher repeate decrease will mean that a 2s and 3s will be less likely to appear within a context of all 1s '''
        self.width = width
        self.height = height
        self.verbose = verbose
        self.color = color
        self.final_grid = []
        self.default_distro = distro
        self.above_bias = above_bias
        self.diag_bias = diag_bias
        self.side_bias = side_bias
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
                print formated, #'\t',
            print #'\n'   

    def __str__(self):
        string_grid = ''
        for row in self.final_grid:
            for i in row:
                hue = self.colors[i]
                string_grid += ''.join(str(i)) + '\t'
            string_grid += ('\n'+'\n')
        return string_grid

    def _choose_cell(self, i, k):
        if i == 0:
            cell = random.choice(self.dict_to_list(self.default_distro))
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
            if cell == 2 and upper_left != 2 and above != 2 and upper_right != 2 and self.default_distro[2] >= self.repeat_decrease:
                self._half_distro(2)
            if cell == 3 and upper_left != 3 and above != 3 and upper_right != 3 and self.default_distro[3] >= self.repeat_decrease:
                self._half_distro(3)
        return cell    

    def _create_distro(self, upper_left, above, upper_right, side):

        distro = copy.deepcopy(self.default_distro)

        over_index = distro.get(above,0)
        over_index += self.above_bias
        distro[above] = over_index
        one_index = distro[1]
        one_index -= self.above_bias
        distro[1] = one_index 

        if upper_left:
            left_index = distro.get(upper_left,0)
            left_index += self.diag_bias
            distro[upper_left] = left_index
            one_index = distro[1]
            one_index -= self.diag_bias
            distro[1] = one_index 

        if upper_right:        
            right_index = distro.get(upper_right,0)
            right_index += self.diag_bias
            distro[upper_right] = right_index
            one_index = distro[1]
            one_index -= self.diag_bias
            distro[1] = one_index

        if side:
            side_index = distro.get(side,0)
            side_index += self.side_bias
            distro[side] = side_index
            one_index = distro[1]
            one_index -= self.side_bias
            distro[1] = one_index
        
        possibles = self.dict_to_list(distro)
        return possibles

    def _half_distro(self, key):
        val = self.default_distro[key]
        new_val = val/self.repeat_decrease
        self.default_distro[key] = new_val
        
    def dict_to_list(self, seq):
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
