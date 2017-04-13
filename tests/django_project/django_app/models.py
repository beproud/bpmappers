from django.db import models


class M2M_ParentModel(models.Model):
    bacon = models.ManyToManyField('M2M_ChildModel')


class M2M_ChildModel(models.Model):
    spam = models.CharField(max_length=30)


class M2M_Through_ParentModel(models.Model):
    bacon = models.ManyToManyField(
        'M2M_Through_ChildModel', through='M2M_ThroughModel')


class M2M_Through_ChildModel(models.Model):
    spam = models.CharField(max_length=30)


class M2M_ThroughModel(models.Model):
    child = models.ForeignKey('M2M_Through_ChildModel')
    parent = models.ForeignKey('M2M_Through_ParentModel')
    knight = models.CharField(max_length=30)
