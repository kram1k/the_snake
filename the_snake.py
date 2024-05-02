"""Модуль для рандомного появления предметов."""
from random import choice, randint
import sys
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Рандомное направление змейки
random_direction = choice(seq=[RIGHT, LEFT, UP, DOWN])


# Тут опишите все классы игры.
class GameObject():
    """
    Это базовый класс.

    От этого наследуются другие игровые объекты.
    """

    body_color: tuple
    GameObject = None

    def __init__(self, position=SCREEN_CENTER,
                 body_color=BOARD_BACKGROUND_COLOR):
        """Иницилизатор класса GameObject."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Этот метод должен определять.

        Как объект будет отрисовываться на экране.
        """
        pass


class Apple(GameObject):
    """
    Класс, унаследованный от GameObject.

    Описывающий яблоко и действия с ним.
    Яблоко должно отображаться в случайных клетках игрового поля.
    """

    def __init__(self):
        """Иницилизатор класса Apple."""
        self.x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (self.x, self.y)
        return self.position

    def draw(self):
        """Метод draw класса Apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс, унаследованный от GameObject.

    Описывающий змейку и действия с ней.
    По умолчанию хмейка находится в центре экрана.
    """

    def __init__(self, body_color=SNAKE_COLOR,
                 length=1, direction=RIGHT, next_direction=None, last=None):
        """Иницилизатор класса Snake."""
        super().__init__()
        self.positions = [self.position]
        self.body_color = body_color
        self.length = length
        self.direction = direction
        self.next_direction = next_direction
        self.last = last

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод возвращающий позицию головы змейки."""
        result = self.positions[0]
        return result

    def reset(self):
        """
        Cбрасывает змейку в начальное состояние.

        После столкновения с собой.
        """
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = random_direction

    def move(self):
        """Обновляет положение змейки в игре."""
        head = self.get_head_position()
        new_head_x = self.direction[0]
        new_head_y = self.direction[1]
        new_head = ((
            head[0] + new_head_x * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + new_head_y * GRID_SIZE) % SCREEN_HEIGHT)

        # Обновление списка позиций
        self.positions.insert(0, new_head)
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Метод draw класса Snake."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object, event):
    """Функция обработки действий пользователя"""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and game_object.direction != DOWN:
            game_object.next_direction = UP
        elif event.key == pygame.K_DOWN and game_object.direction != UP:
            game_object.next_direction = DOWN
        elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
            game_object.next_direction = LEFT
        elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
            game_object.next_direction = RIGHT


def check_collision(snake, apple):
    """Проверяет, столкнулась ли змейка с яблоком."""
    snake_head = snake.get_head_position()
    if snake_head == apple.position:
        snake.length += 1
        apple.randomize_position()


def main():
    """Основной игровой цикл"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            handle_keys(snake, event)
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.update_direction()
            snake.move()
            snake.draw()
            apple.draw()
            check_collision(snake, apple)
            clock.tick(SPEED)
            pygame.display.update()


if __name__ == '__main__':
    main()
