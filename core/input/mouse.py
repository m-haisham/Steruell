import pygame


class Mouse:
    instance = None

    def __init__(self):
        Mouse.instance = self

        self.down = [0, 0, 0]

        self.left = MouseButton()
        self.middle = MouseButton()
        self.right = MouseButton()

    def update(self):
        down = pygame.mouse.get_pressed()

        self.left = MouseButton.calculate(down[0], self.down[0])
        self.middle = MouseButton.calculate(down[1], self.down[1])
        self.right = MouseButton.calculate(down[2], self.down[2])

        self.down = down


class MouseButton:
    def __init__(self, pressed=False, released=False, down=False):
        self.pressed = pressed
        self.released = released
        self.down = down

    @staticmethod
    def calculate(now, previous):
        button = MouseButton()

        if now:
            button.down = True

        if not previous and now:
            button.pressed = True
        if previous and not now:
            button.released = True

        return button

    def __str__(self):
        return f'<MouseButton{dict(pressed=self.pressed, released=self.released, dowm=self.down)}>'