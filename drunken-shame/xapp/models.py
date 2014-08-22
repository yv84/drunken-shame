# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from datetime import date

from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _


yaml_types = {
    'char': 'CharField',
    'int': 'IntegerField',
    'date': 'DateField',
}


class Users(models.Model):
    class Meta:
        verbose_name = _(u'Пользователи')
        verbose_name_plural = _(u'Пользователи')

    name = models.CharField(max_length=100, verbose_name = _(u"Имя"))
    paycheck = models.IntegerField(verbose_name=_("Зарплата"))
    date_joined = models.DateField(auto_now=False, auto_now_add=False,
        verbose_name = _(u"Дата поступления на работу"),)

    def __str__(self):
        return u"{0}".format(self.name)

    @staticmethod
    def field_name(cls, field):
        return User._meta.get_field(field).verbose_name

    def get_absolute_url(self):
        return reverse('xapp:user:detail', kwargs={'pk': self.pk})


class Rooms(models.Model):
    class Meta:
        verbose_name = _(u'Комнаты')
        verbose_name_plural = _(u'Комнаты')

    department = models.CharField(max_length=100,
        verbose_name = _(u"Отдел"),)
    spots = models.IntegerField(verbose_name=_(u"Вместимость"))

    def __str__(self):
        return u"{0}".format(self.department)

    def get_absolute_url(self):
        return reverse('xapp:room:detail', kwargs={'pk': self.pk})



tables = []
tables.append(Users)
tables.append(Rooms)
