class Player:
    def __init__(self):
        self.score = 0
        self.level = 1

    def add_score(self, points):
        self.score += points

    def get_status(self):
        return f"Score: {self.score}, Level: {self.level}"
