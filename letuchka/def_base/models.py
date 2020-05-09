from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний ID пользователя',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Имя пользователя'
    )

    def __str__(self):
        return f'{self.id}'  # {self.external_id}
        # return f'#{self.external_id} {self.name}'   # def_base.Profile

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Category(models.Model):
    profile = models.ForeignKey(
        to='def_base.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    category = models.TextField(
        verbose_name='Категория',
    )

    set_category = models.TextField(
        verbose_name='Параметры',
        default='1, 1',
    )

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Definition(models.Model):
    profile = models.ForeignKey(
        to='def_base.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    category = models.TextField(
        verbose_name='Категория',
        default='The category',

    )
    header = models.TextField(
        verbose_name='Заголовок',
    )
    question = models.TextField(
        verbose_name='Заголовок',
        default='The question',
    )

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'Опредление'
        verbose_name_plural = 'Опредления'

