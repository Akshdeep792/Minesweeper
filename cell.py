from tkinter import *
import random
import turtle
import settings
import ctypes
import sys



class Cell:
    
    cell_list = []
    cell_count = settings.CELL_COUNTS
    cell_count_label_object = None

    
    def __init__(self,x,y, is_Mine=False) :
        self.is_Mine = is_Mine
        self.is_open = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        #append the object to Cell.cell_list
        Cell.cell_list.append(self)


    def create_btn_object(self, position):
        btn = Button(
            position,
            width=12,
            height=4,
            
        )
        btn.bind('<Button-1>', self.left_actions)
        btn.bind('<Button-3>', self.right_actions)

        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            text=f"Cells Left: {Cell.cell_count}",
            bg="black",
            fg="white",
            width=12,
            height=4,
            font=("", 30)
            
        )

        Cell.cell_count_label_object = lbl

    
    def left_actions(self,event):
        if self.is_Mine:
            self.show_Mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cell:
                    cell_obj.show_cell()
            self.show_Cell()
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You won the game!', 'Game Over', 0)

        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')
        
    def show_Mine(self):
        self.cell_btn_object.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over', 0)
        sys.exit()

        
    def get_cell_by_axis(self, x, y):
        #return a cell object
        for cell in Cell.cell_list:
            if cell.x == x and cell.y == y:
                return cell


    @property
    def surrounded_cell(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y -1),
            self.get_cell_by_axis(self.x + 1, self.y ),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)

        ]

        # for out of bound cases
        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_length(self) -> int:
        counter = 0
        for cell in self.surrounded_cell:
            if cell.is_Mine:
                counter+=1
        
        return counter


    def show_Cell(self):
        if not self.is_open:
            Cell.cell_count -=1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
                #replace cell count label to new count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left: {Cell.cell_count}"
                )

            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )
            
        self.is_open = True
        

    def right_actions(self,event):

        if not self.is_mine_candidate:
            self.cell_btn_object.configure(bg='orange');
        
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )
            self.is_mine_candidate = False


    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.cell_list,
            settings.MINES_COUNT
            
        )
        for picked_cell in picked_cells:
            picked_cell.is_Mine = True

        
    def __repr__(self):
        return f"Cell [{self.x}, {self.y}]"