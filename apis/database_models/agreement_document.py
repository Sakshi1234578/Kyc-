from django.db import models


class AgreementDocument(models.Model):
    document_id = models.AutoField(primary_key=True, db_column='document_id')
    merchant_id = models.ForeignKey('merchant_data', on_delete=models.CASCADE, null=True, db_column='merchant_id')
    login_id = models.IntegerField(null=True, db_column='login_id')
    name = models.CharField(max_length=100, null=True)
    file_path = models.CharField(max_length=255, null=True, db_column='file_Path')
    type = models.ForeignKey('DocumentTypeMaster', on_delete=models.CASCADE, null=True, db_column='type')
    is_latest = models.BooleanField(null=True, db_column='is_Latest')
    created_by = models.IntegerField(null=True, db_column='created_by')
    created_date = models.DateTimeField(null=False, auto_now_add=True, db_column='created_date')
    modified_date = models.DateTimeField(null=True, auto_now=False, db_column='modified_date')
    modified_by = models.IntegerField(null=True, db_column='modified_by')
    status = models.CharField(max_length=50, null=True)
    comment = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'agreement_document'
