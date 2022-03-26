import pygame
import random 

pygame.init()

class DrawInfomation:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0, 137, 123
    RED = 255,0,0
    PURPLE = 177, 96, 238
    BLUE = 64, 99, 216
    BG_COLOR = 45, 45, 45

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont("comicsans", 16)
    BOLD = pygame.font.SysFont("comicsans", 20)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self , width, height, lst):
        self.width = width
        self.height = height 

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst 
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = int((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x =self.SIDE_PAD // 2

def draw(draw_info):
    draw_info.window.fill(draw_info.BG_COLOR)

    controls = draw_info.FONT.render("R - reset | SPACE - start sorting | A - ascending | D - decending", 1, draw_info.BLACK)
    draw_info.window.blit(controls,(draw_info.width/2 - controls.get_width()/2, 5))

    sorting = draw_info.FONT.render("I - insertion sort | B - bubblesort sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 35))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_position={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                        draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BG_COLOR, clear_rect)

    for i,val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_position:
            color = color_position[i]


        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height ))

    if clear_bg:
        pygame.display.update()



def generate_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst 


def bubble_sort(draw_info, ascend=True):
    lst = draw_info.lst 

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascend) or (num1 < num2 and not ascend):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.BLUE}, True)
                yield True

    return lst 

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_list(n, min_val, max_val)
    draw_info = DrawInfomation(800, 600, lst)
    sorting = False
    ascend = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascend)
            elif event.key == pygame.K_a and not sorting:
                ascend = True
            elif event.key == pygame.K_d and not sorting:
                ascend = False
                


    pygame.quit()

if __name__ == "__main__":
    main()
