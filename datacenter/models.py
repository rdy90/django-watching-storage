from django.db import models
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f"{self.owner_name} (inactive)"


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def get_duration(self):
        return localtime() - self.entered_at

    def format_duration(self, delta):
        seconds = delta.total_seconds()
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}ч {minutes}мин" if hours != 0 else f"{minutes}мин"

    def is_strange(self):
        if not self.leaved_at:
            return False

        seconds = (self.leaved_at - self.entered_at).seconds
        hours = int(seconds // 3600)
        return True if hours > 0 else False

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                "leaved at " + str(self.leaved_at)
                if self.leaved_at
                else "not leaved"
            ),
        )
