"""Модуль для рандомного появления предметов."""
import typing
import sys
from random import choice, randint

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTIONS = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()

random_direction = choice(seq=[RIGHT, LEFT, UP, DOWN])


class GameObject:
    """
    Это базовый класс.

    От этого наследуются другие игровые объекты.
    """

    def __init__(self, position: tuple = SCREEN_CENTER,
                 body_color: tuple = BOARD_BACKGROUND_COLOR):
        """Иницилизатор класса GameObject."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Этот метод должен определять.

        Как объект будет отрисовываться на экране.
        """


class Snake(GameObject):
    """
    Класс, унаследованный от GameObject.

    Описывающий змейку и действия с ней.
    По умолчанию хмейка находится в центре экрана.
    """

    def __init__(self, length=1, direction=RIGHT, next_direction=None,
                 last=None, body_color=SNAKE_COLOR,
                 position=SCREEN_CENTER):
        """Иницилизатор класса Snake."""
        super().__init__(position=position, body_color=body_color)
        self.positions = [self.position]
        self.length = length
        self.direction = direction
        self.next_direction = next_direction
        self.last = last
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод возвращающий позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """
        Cбрасывает змейку в начальное состояние.

        После столкновения с собой.
        """
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = random_direction

    def check_crash(self):
        """Проверяет, столкнулась ли змейка с собой."""
        if self.get_head_position() in self.positions[1:]:
            self.reset()

    def move(self):
        """Обновляет положение змейки в игре."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = ((
            head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT)

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
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """
    Класс, унаследованный от GameObject.

    Описывающий яблоко и действия с ним.
    Яблоко должно отображаться в случайных клетках игрового поля.
    """

    def __init__(self, position=SCREEN_CENTER, body_color=APPLE_COLOR,
                 occupied_cells: typing.Optional[list] = None):
        """Иницилизатор класса Apple."""
        self.occupied_cells = occupied_cells or []
        super().__init__(body_color=body_color, position=position)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in self.occupied_cells:
                self.position = new_position
            break

    def draw(self):
        """Метод draw класса Apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(snake):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            next_direction = DIRECTIONS.get(event.key)
            if next_direction:
                snake.next_direction = next_direction
    return True


def check_collision(snake, apple):
    """Проверяет, столкнулась ли змейка с яблоком."""
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize_position()


def main():
    """Основной игровой цикл"""
    pygame.init()
    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)
    while True:
        clock.tick(SPEED)
        if handle_keys(snake) is False:
            pygame.quit()
            sys.exit()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.update_direction()
        snake.move()
        snake.check_crash()
        check_collision(snake, apple)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
