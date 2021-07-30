from django.db import models


class PsValues(models.Model):
    pid = models.IntegerField()
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    command = models.CharField(max_length=50)

    class Meta:
        db_table = 'ps_values'
        ordering = ['pid']

    def __str__(self):
        return f"{self.pid} {self.cpu_usage} {self.memory_usage} {self.created_at} {self.command}"
