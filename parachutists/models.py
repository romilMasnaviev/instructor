from django.db import models
from accounts.models import Account

class Parachutist(models.Model):
    parachutist_id = models.AutoField(primary_key=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, db_column='account_id')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    refusal_reason = models.TextField(blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'parachutist'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ParachutistStatusHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    parachutist = models.ForeignKey(Parachutist, on_delete=models.CASCADE, db_column='parachutist_id')
    status = models.CharField(max_length=255)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'parachutist_status_history'
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.parachutist} - {self.status} ({self.changed_at})"