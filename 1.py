import pygame
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
BLOCK_SIZE = 60
HUD_HEIGHT = 120
MIN_SCREEN_WIDTH = 8 * BLOCK_SIZE
MIN_SCREEN_HEIGHT = 7 * BLOCK_SIZE + HUD_HEIGHT

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# 游戏对象类型
WALL = 1
PLAYER = 2
BOX = 3
TARGET = 4
PLAYER_ON_TARGET = 5
BOX_ON_TARGET = 6
FLOOR = 0
VOID = -1

# 10 个递增难度的关卡。使用经典推箱子布局，并在加载时自动剔除外围无效空白区域。
levels = [
    [
        [1, 1, 1, 1, 0, 0],
        [1, 0, 4, 1, 0, 0],
        [1, 0, 0, 1, 1, 1],
        [1, 6, 2, 0, 0, 1],
        [1, 0, 0, 3, 0, 1],
        [1, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 0],
    ],
    [
        [1, 1, 1, 1, 1, 0],
        [1, 4, 0, 0, 1, 1],
        [1, 2, 3, 3, 0, 1],
        [1, 1, 0, 0, 0, 1],
        [0, 1, 1, 0, 0, 1],
        [0, 0, 1, 1, 4, 1],
        [0, 0, 0, 1, 1, 1],
    ],
    [
        [0, 0, 1, 1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 3, 0, 1],
        [1, 0, 1, 0, 0, 1, 3, 0, 1],
        [1, 0, 4, 0, 4, 1, 2, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 1, 2, 0, 1],
        [1, 0, 3, 6, 0, 1],
        [1, 0, 4, 6, 0, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 4, 6, 6, 3, 2, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 1],
        [0, 0, 0, 0, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
        [1, 0, 3, 3, 0, 0, 0, 0, 0, 1, 2, 1],
        [1, 0, 3, 0, 1, 4, 4, 4, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    ],
    [
        [0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 1, 0, 4, 4, 2, 1],
        [0, 0, 1, 0, 3, 3, 0, 1],
        [0, 0, 1, 1, 0, 1, 1, 1],
        [0, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0],
        [1, 1, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 1, 0],
        [1, 0, 1, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 1, 0],
        [1, 1, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
    ],
    [
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 4, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 4, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 4, 1, 0, 1],
        [1, 0, 2, 0, 3, 0, 3, 0, 3, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    ],
    [
        [0, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 4, 3, 4, 0, 1],
        [1, 1, 0, 3, 2, 3, 0, 1],
        [1, 0, 0, 4, 3, 4, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 4, 3, 4, 0, 1],
        [1, 0, 3, 4, 3, 0, 1],
        [1, 0, 4, 3, 4, 0, 1],
        [1, 0, 3, 4, 3, 0, 1],
        [1, 0, 0, 2, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ],
]


def flood_fill_outside(grid):
    """把从边界可达的空白地板标记为 VOID，用于隐藏关卡外填充区域。"""
    height = len(grid)
    width = len(grid[0])
    stack = []
    visited = set()

    for x in range(width):
        stack.append((x, 0))
        stack.append((x, height - 1))
    for y in range(height):
        stack.append((0, y))
        stack.append((width - 1, y))

    while stack:
        x, y = stack.pop()
        if (x, y) in visited or not (0 <= x < width and 0 <= y < height):
            continue
        if grid[y][x] != FLOOR:
            continue
        visited.add((x, y))
        grid[y][x] = VOID
        stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])


def validate_levels(level_list):
    """检查关卡的玩家、箱子和目标点配置是否合理。"""
    for index, level in enumerate(level_list, start=1):
        widths = {len(row) for row in level}
        if len(widths) != 1:
            raise ValueError(f'Level {index} 的每一行长度必须一致')

        player_count = sum(cell in (PLAYER, PLAYER_ON_TARGET) for row in level for cell in row)
        box_count = sum(cell in (BOX, BOX_ON_TARGET) for row in level for cell in row)
        target_count = sum(cell in (TARGET, PLAYER_ON_TARGET, BOX_ON_TARGET) for row in level for cell in row)

        if player_count != 1:
            raise ValueError(f'Level {index} 必须且只能有 1 个玩家，当前为 {player_count}')
        if box_count == 0:
            raise ValueError(f'Level {index} 至少需要 1 个箱子')
        if box_count != target_count:
            raise ValueError(f'Level {index} 的箱子数 ({box_count}) 与目标点数 ({target_count}) 不一致')


validate_levels(levels)

class SokobanGame:
    def __init__(self, level=0):
        self.screen = None
        pygame.display.set_caption("推箱子游戏")
        self.clock = pygame.time.Clock()
        self.current_level = level
        self.map_offset_x = 0
        self.map_offset_y = 0
        self.restart_button_rect = pygame.Rect(0, 0, 0, 0)
        self.load_level()
        
    def load_level(self):
        """加载当前关卡"""
        self.grid = [row[:] for row in levels[self.current_level]]
        flood_fill_outside(self.grid)
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        self.update_display()
        
        # 找到玩家位置
        self.find_player()
        
        # 计算总箱子数和目标点数
        self.box_count = sum(row.count(3) + row.count(6) for row in self.grid)
        self.target_count = sum(row.count(4) + row.count(5) + row.count(6) for row in self.grid)

    def update_display(self):
        """根据关卡大小动态调整窗口，并计算地图绘制偏移。"""
        map_width = self.width * BLOCK_SIZE
        map_height = self.height * BLOCK_SIZE
        screen_width = max(MIN_SCREEN_WIDTH, map_width)
        screen_height = max(MIN_SCREEN_HEIGHT, map_height + HUD_HEIGHT)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.map_offset_x = (screen_width - map_width) // 2
        self.map_offset_y = HUD_HEIGHT
        
    def find_player(self):
        """找到玩家的位置"""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == PLAYER or self.grid[y][x] == PLAYER_ON_TARGET:
                    self.player_x = x
                    self.player_y = y
                    return
                    
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(BLACK)
        self.draw_hud()
        
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    self.map_offset_x + x * BLOCK_SIZE,
                    self.map_offset_y + y * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
                
                if self.grid[y][x] == WALL:
                    pygame.draw.rect(self.screen, BROWN, rect)
                elif self.grid[y][x] == PLAYER:
                    pygame.draw.rect(self.screen, BLUE, rect)
                    pygame.draw.circle(self.screen, YELLOW, 
                                     rect.center,
                                     BLOCK_SIZE//3)
                elif self.grid[y][x] == BOX:
                    pygame.draw.rect(self.screen, BROWN, rect)
                    pygame.draw.rect(self.screen, BLACK, rect.inflate(-10, -10))
                elif self.grid[y][x] == TARGET:
                    pygame.draw.rect(self.screen, GRAY, rect)
                    pygame.draw.circle(self.screen, RED, 
                                     rect.center,
                                     BLOCK_SIZE//4)
                elif self.grid[y][x] == PLAYER_ON_TARGET:
                    pygame.draw.rect(self.screen, GRAY, rect)
                    pygame.draw.circle(self.screen, YELLOW, 
                                     rect.center,
                                     BLOCK_SIZE//3)
                elif self.grid[y][x] == BOX_ON_TARGET:
                    pygame.draw.rect(self.screen, GRAY, rect)
                    pygame.draw.rect(self.screen, BROWN, rect.inflate(-10, -10))
                    pygame.draw.circle(self.screen, GREEN, 
                                     rect.center,
                                     BLOCK_SIZE//4)
                elif self.grid[y][x] == FLOOR:
                    pygame.draw.rect(self.screen, WHITE, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 1)
                    
        font = pygame.font.Font(None, 36)
        if self.check_victory():
            victory_text = font.render("VICTORY! Press Space for next level", True, YELLOW)
            text_rect = victory_text.get_rect(center=(self.screen.get_width() // 2, HUD_HEIGHT // 2))
            self.screen.blit(victory_text, text_rect)
        elif self.is_deadlock():
            deadlock_text = font.render("Deadlock! Click Restart or press R", True, RED)
            text_rect = deadlock_text.get_rect(center=(self.screen.get_width() // 2, HUD_HEIGHT // 2))
            self.screen.blit(deadlock_text, text_rect)

    def draw_hud(self):
        """绘制顶部信息栏和重开按钮。"""
        hud_rect = pygame.Rect(0, 0, self.screen.get_width(), HUD_HEIGHT)
        pygame.draw.rect(self.screen, (30, 30, 30), hud_rect)
        pygame.draw.line(self.screen, WHITE, (0, HUD_HEIGHT - 2), (self.screen.get_width(), HUD_HEIGHT - 2), 2)

        title_font = pygame.font.Font(None, 36)
        info_font = pygame.font.Font(None, 28)

        level_text = title_font.render(f"Level: {self.current_level + 1} / {len(levels)}", True, WHITE)
        hint_text = info_font.render("Arrow keys: Move   R: Restart   Space: Next level", True, WHITE)
        self.screen.blit(level_text, (20, 18))
        self.screen.blit(hint_text, (20, 58))

        button_width = 150
        button_height = 48
        self.restart_button_rect = pygame.Rect(
            self.screen.get_width() - button_width - 20,
            26,
            button_width,
            button_height
        )
        pygame.draw.rect(self.screen, RED, self.restart_button_rect, border_radius=8)
        pygame.draw.rect(self.screen, WHITE, self.restart_button_rect, 2, border_radius=8)

        button_text = info_font.render("下一关", True, WHITE)
        button_text_rect = button_text.get_rect(center=self.restart_button_rect.center)
        self.screen.blit(button_text, button_text_rect)
                    
    def move(self, dx, dy):
        """移动玩家"""
        new_x = self.player_x + dx
        new_y = self.player_y + dy

        if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.height:
            return
        
        # 检查新位置是否为墙
        if self.grid[new_y][new_x] in (WALL, VOID):
            return
            
        # 检查新位置是否为箱子
        if self.grid[new_y][new_x] == BOX or self.grid[new_y][new_x] == BOX_ON_TARGET:
            push_x = new_x + dx
            push_y = new_y + dy
            
            # 检查箱子新位置是否可以移动
            if (push_x < 0 or push_x >= self.width or push_y < 0 or push_y >= self.height or
                self.grid[push_y][push_x] in (WALL, VOID) or
                self.grid[push_y][push_x] == BOX or self.grid[push_y][push_x] == BOX_ON_TARGET):
                return
                
            # 移动箱子
            if self.grid[push_y][push_x] == TARGET:
                self.grid[push_y][push_x] = BOX_ON_TARGET
            else:
                self.grid[push_y][push_x] = BOX
                
            # 原来的箱子位置变成玩家或玩家在目标点
            if self.grid[new_y][new_x] == BOX_ON_TARGET:
                self.grid[new_y][new_x] = PLAYER_ON_TARGET
            else:
                self.grid[new_y][new_x] = PLAYER
        else:
            # 移动玩家
            if self.grid[new_y][new_x] == TARGET:
                self.grid[new_y][new_x] = PLAYER_ON_TARGET
            else:
                self.grid[new_y][new_x] = PLAYER
                
        # 清除旧玩家位置
        if self.grid[self.player_y][self.player_x] == PLAYER_ON_TARGET:
            self.grid[self.player_y][self.player_x] = TARGET
        else:
            self.grid[self.player_y][self.player_x] = FLOOR
            
        self.player_x = new_x
        self.player_y = new_y
        
    def check_victory(self):
        """检查是否胜利（所有箱子都在目标点上）"""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == BOX:
                    return False
        return True

    def is_blocking(self, x, y):
        """判断一个位置是否会阻挡箱子。边界视作墙。"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.grid[y][x] in (WALL, VOID, BOX, BOX_ON_TARGET)

    def is_deadlock(self):
        """基础死局检测：非目标点上的箱子被卡在角落。"""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] != BOX:
                    continue
                if ((self.is_blocking(x - 1, y) and self.is_blocking(x, y - 1)) or
                    (self.is_blocking(x - 1, y) and self.is_blocking(x, y + 1)) or
                    (self.is_blocking(x + 1, y) and self.is_blocking(x, y - 1)) or
                    (self.is_blocking(x + 1, y) and self.is_blocking(x, y + 1))):
                    return True
        return False
        
    def reset_level(self):
        """重置当前关卡"""
        self.load_level()
        
    def next_level(self):
        """进入下一关"""
        self.current_level += 1
        if self.current_level >= len(levels):
            self.current_level = 0
        self.load_level()
        
    def run(self):
        """游戏主循环"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.restart_button_rect.collidepoint(event.pos):
                        self.reset_level()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.move(0, 1)
                    elif event.key == pygame.K_LEFT:
                        self.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move(1, 0)
                    elif event.key == pygame.K_r:
                        self.reset_level()
                    elif event.key == pygame.K_SPACE and self.check_victory():
                        self.next_level()
                        
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SokobanGame(0)
    game.run()

