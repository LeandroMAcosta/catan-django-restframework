from django.db import models


class Road(models.Model):
    owner = models.ForeignKey("player.Player", on_delete=models.CASCADE)
    v1 = models.ForeignKey(
        "board.Vertex", on_delete=models.CASCADE, related_name='road_in')
    v2 = models.ForeignKey(
        "board.Vertex", on_delete=models.CASCADE, related_name='road_out')

    def __str__(self):
        return "Road {0} {1} {2}"
        return "Road " + str(self.v1) + " " + str(self.v2) + " from "
        + str(self.owner)

    class Meta:
        unique_together = ['owner', 'v1', 'v2']
