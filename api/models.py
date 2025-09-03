from django.db import models
from accounts.models import CustomUser

class Transaction(models.Model):
    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey(CustomUser,related_name='user_transactions' ,on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now=True)

    def str(self):
        return self.title
    
    class Meta:
        db_table = 'transaction'
        managed = True
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'