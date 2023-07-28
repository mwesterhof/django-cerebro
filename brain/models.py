from django.db import models


class VisitorBehavior(models.Model):
    time_spent = models.IntegerField()
    pages_visited = models.IntegerField()

    conversion_target_a = models.IntegerField(default=0)
    conversion_target_b = models.IntegerField(default=0)

    @property
    def sample(self):
        return [int(self.time_spent), int(self.pages_visited)]

    @property
    def feature(self):
        return [int(self.conversion_target_a), int(self.conversion_target_b)]

    def __str__(self):
        return f'<Behavior time_spent: {self.time_spent} pages_visited: {self.pages_visited}>'
