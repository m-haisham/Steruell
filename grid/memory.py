import pygame
from pathlib import Path

from core.memory import JsonMemory


class AppDatabase(JsonMemory):
    instance = None

    def __init__(self):
        super(AppDatabase, self).__init__(Path('data.db'))

    def save_grid(self, key, grid, drawable):
        self.put(key, (grid, drawable))
        self.save()

    def load_grid(self, key):
        try:
            return self.get(key)
        except KeyError:
            return None

    @staticmethod
    def database():
        """
        :return: database instance
        :rtype: AppDatabase
        """
        if AppDatabase.instance is None:
            AppDatabase.instance = AppDatabase()

        return AppDatabase.instance


key_map = {
    pygame.K_0: '0',
    pygame.K_1: '1',
    pygame.K_2: '2',
    pygame.K_3: '3',
    pygame.K_4: '4',
    pygame.K_5: '5',
    pygame.K_6: '6',
    pygame.K_7: '7',
    pygame.K_8: '8',
    pygame.K_9: '9',
}
