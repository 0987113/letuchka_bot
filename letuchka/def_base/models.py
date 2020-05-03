from django.db import models

# Create your models here.


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


class Definition(models.Model):
    profile = models.ForeignKey(
        to='def_base.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    created_at = models.DateTimeField(
        verbose_name='Время получения',
        auto_now_add=True,
    )
    header_def = models.TextField(
        verbose_name='Заголовок',
    )   # default='The header',

    def __str__(self):
        return f'Определение {self.pk} от {self.profile}'

    class Meta:
        verbose_name = 'Опредление'
        verbose_name_plural = 'Опредления'


class Category(models.Model):
    profile = models.ForeignKey(
        to='def_base.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    category = models.TextField(
        verbose_name='Категория',
    )

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
