# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from datetime import date

from django.db import models
from django.utils.translation import ugettext as _


class Room(models.Model):
    class Meta:
        verbose_name = _(u'Комната')
        verbose_name_plural = _(u'Комнаты')

    department = models.CharField(max_length=100,
        help_text = _(u"Отдел"),)
    spots = models.IntegerField(help_text=_(u"Вместимость"))

    def __str__(self):
        return u"{0}".format(self.department)


class User(models.Model):
    class Meta:
        verbose_name = _(u'Пользователь')
        verbose_name_plural = _(u'Пользователи')

    name = models.CharField(max_length=100, help_text = _(u"Имя"))
    paycheck = models.IntegerField(help_text = _(u"Зарплата"))
    date_joined = models.DateField(auto_now=False, auto_now_add=False,
        help_text = _(u"Дата поступления на работу"),)

    def __str__(self):
        return u"{0}".format(self.name)
