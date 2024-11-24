import pygame

class Clock:
    # one tick is 10 minutes -> 5s
    def __init__(self):
        self.tick = 48

    def period(self):
        hour = (self.tick % 144) // 6
        if (hour < 8 and hour >= 0) or hour >= 23:
            return "bedtime"
        elif hour >= 18:
            return "night"
        elif hour >= 32:
            return "afternoon"
        else:
            return "morning"

    def day(self):
        return self.tick // 144 + 1

    def hour(self):
        return (self.tick % 144) // 6

    def minute(self):
        return (self.tick % 6) * 10