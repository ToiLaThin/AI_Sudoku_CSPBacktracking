from back import *
from time import sleep
import pygame
# region GLOBAL VAR
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
BLOCK_SIZE = 40

IDX_ROW = 0
IDX_COL = 0
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Sudoku")

# init font && create Font object
pygame.init()
FONT = pygame.font.SysFont('comicsans', 18, bold=False, italic=False)
FPS = 60
# endregion
# TODO CHỈNH SỬA HÀM NÀO GLOBAL INIT_ASSIGN
# liên quan init_assign


def draw_grid(init_assign: str):
    # draw vertical lines
    for col in range(0, 10):
        if col % 3 == 0:
            thick = 5
        else:
            thick = 2
        pygame.draw.line(WIN, COLOR_BLACK, [
                         col * BLOCK_SIZE, 0], [col * BLOCK_SIZE, 9*BLOCK_SIZE], width=thick)

    # draw horizontal lines
    for row in range(0, 10):
        if row % 3 == 0:
            thick = 5
        else:
            thick = 2
        pygame.draw.line(WIN, COLOR_BLACK, [
                         0, row * BLOCK_SIZE], [9 * BLOCK_SIZE, row * BLOCK_SIZE], width=thick)

    squares = re.findall(r'\d|\.', init_assign)
    for idx in range(0, len(squares)):
        if squares[idx] != '.':
            val = int(squares[idx])
        else:
            val = 0
        idx_row = idx // 9
        idx_col = idx % 9
        draw_val(val, idx_col, idx_row, COLOR_BLACK)


def get_cord():
    global IDX_ROW, IDX_COL
    pos = pygame.mouse.get_pos()
    # tung
    IDX_ROW = pos[1] // BLOCK_SIZE

    # hoanh
    IDX_COL = pos[0] // BLOCK_SIZE


def draw_red_box():
    global IDX_ROW, IDX_COL
    # top left point cords
    y = IDX_ROW * BLOCK_SIZE
    x = IDX_COL * BLOCK_SIZE

    # 2 hori line
    pygame.draw.line(WIN, COLOR_RED, [x, y], [x + BLOCK_SIZE, y], width=5)
    pygame.draw.line(WIN, COLOR_RED, [
                     x, y + BLOCK_SIZE], [x + BLOCK_SIZE, y + BLOCK_SIZE], width=5)

    # 2 verti line
    pygame.draw.line(WIN, COLOR_RED, [x, y], [x, y + BLOCK_SIZE], width=5)
    pygame.draw.line(WIN, COLOR_RED, [
                     x + BLOCK_SIZE, y], [x + BLOCK_SIZE, y + BLOCK_SIZE], width=5)


def get_val_pressed(key_pressed):
    if key_pressed[pygame.K_1]:
        val = 1
    if key_pressed[pygame.K_2]:
        val = 2
    if key_pressed[pygame.K_3]:
        val = 3
    if key_pressed[pygame.K_4]:
        val = 4
    if key_pressed[pygame.K_5]:
        val = 5
    if key_pressed[pygame.K_6]:
        val = 6
    if key_pressed[pygame.K_7]:
        val = 7
    if key_pressed[pygame.K_8]:
        val = 8
    if key_pressed[pygame.K_9]:
        val = 9
    return val


def draw_val(val: int, x, y, color):
    global FONT
    if 0 < val <= 9:
        text = FONT.render(str(val), True, color)
        WIN.blit(text, [x * BLOCK_SIZE + 15, y*BLOCK_SIZE + 10])


def cord_is_valid(init_assign: str):
    border_up = 0
    border_left = 0
    border_down = 9 * BLOCK_SIZE
    border_right = 9 * BLOCK_SIZE

    if border_left <= IDX_COL * BLOCK_SIZE <= border_right - BLOCK_SIZE and border_up <= IDX_ROW * BLOCK_SIZE <= border_down - BLOCK_SIZE:
        idx_init_assign = IDX_ROW * 9 + IDX_COL
        if init_assign[idx_init_assign] == '.':
            return True
        else:
            return False
    else:
        return False

# liên quan init_assign


def game_loop(init_assign: str):
    clock = pygame.time.Clock()
    running = True
    clicked = False
    pressed = False
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            WIN.fill(COLOR_WHITE)
            draw_grid(init_assign)

            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                get_cord()
                # để nhập nút mới chứ ko bắt buộc là nút vừa rồi
                pressed = False
                clicked = True

            # Ấn enter thì dùng backtracking search giải
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    sudoku = MySudoku(init_assign)
                    if backtracking_search(sudoku) == None:
                        WIN.fill(COLOR_RED)
                        pygame.display.update()
                        sleep(2)
                    else:
                        sleep(5)
                        WIN.fill(COLOR_GREEN)
                        pygame.display.update()
                        sleep(2)
                elif event.key == pygame.K_r:
                    init_assign = '.91.7....2.3....5....4.29.7..28.6..9.........9..1.46..1.52.7....8....5.1....1.76.'

            if event.type == pygame.KEYDOWN and clicked:
                key_pressed = pygame.key.get_pressed()
                pressed = True

            if clicked:
                if cord_is_valid(init_assign):
                    draw_red_box()
                    if pressed:
                        val_pressed = get_val_pressed(key_pressed)
                        draw_val(val_pressed, IDX_COL, IDX_ROW, COLOR_RED)

                        # thay đổi luôn init_assign
                        idx_init_assign = IDX_ROW * 9 + IDX_COL
                        init_assign = init_assign[:idx_init_assign] + \
                            str(val_pressed) + \
                            init_assign[idx_init_assign + 1:]

                elif not cord_is_valid(init_assign):
                    clicked = False
                    pressed = False

            pygame.display.update()


# class kế thừa sudoku để có thể lấy được chuỗi thể hiện các giá trị có trong các ô hiện tại


class MySudoku(Sudoku):
    def get_grid_string(self):
        result = ''
        for var in self.curr_domains.keys():
            if len(self.curr_domains[var]) > 1:
                result += '.'
            elif len(self.curr_domains[var]) == 1:
                result += str(self.curr_domains[var][0])
        return result

# LIÊN QUAN GLOBAL INIT_ASSIGN


def backtracking_search(csp: MySudoku, select_unassigned_variable=minimum_remaining_values,
                        order_domain_values=least_constraining_value,
                        inference=forward_checking):
    clock = pygame.time.Clock()

    def backtrack(assignment):
        global init_assign
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for val in order_domain_values(var, assignment, csp):
            clock.tick(FPS)
            if csp.nconflicts(var, val, assignment) == 0:
                csp.assign(var, val, assignment)
                removals = csp.get_removals(var, val)
                if inference(csp, var, val, assignment, removals):

                    init_assign = csp.get_grid_string()
                    print(init_assign)
                    draw_grid(init_assign)
                    pygame.display.update()
                    WIN.fill(COLOR_WHITE)

                    result = backtrack(assignment)
                    if result != None:
                        return result
                csp.unassign(var, assignment)
                restore(csp, removals)
        return None
    result = backtrack({})
    return result


if __name__ == '__main__':
    init_assign = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    init_assign = '.91.7....2.3....5....4.29.7..28.6..9.........9..1.46..1.52.7....8....5.1....1.76.'
    game_loop(init_assign)
