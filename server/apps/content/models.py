from django.db import models


class Settings(models.Model):
    primary_color = models.CharField(max_length=20, verbose_name='Primary цвет')
    secondary_color = models.CharField(max_length=20, verbose_name='Вторичный цвет')

    instagram = models.CharField(max_length=80, verbose_name='Ссылка на Instagram')
    telegram = models.CharField(max_length=80, verbose_name='Ссылка на Telegram')
    phone = models.CharField(max_length=25, verbose_name='Номер телефона')
    address = models.CharField(max_length=50, verbose_name='Адрес')

    catalog = models.FileField(upload_to='global/', verbose_name='Презентация (pdf)')
    agreement = models.FileField(upload_to='global/', verbose_name='Пользовательское соглашение')

    meta_description = models.TextField(verbose_name='Мета описание сайта')

    main_title = models.TextField(verbose_name='Заголовок на главной')
    main_subtitle = models.TextField(verbose_name='Подзаголовок на главной')

    main_catalog_title = models.TextField(verbose_name='Заголовок в блоке скачивания')
    main_catalog_text = models.TextField(verbose_name='Текст в блоке скачивания')

    private_order = models.IntegerField(
        verbose_name='Порядок вывода закрытых продаж',
        help_text='Чем выше порядок, тем ниже будет выводиться подборка. Номер должен быть больше 0'
    )
    budget_order = models.IntegerField(
        verbose_name='Порядок вывода подборок по бюджету',
        help_text='Чем выше порядок, тем ниже будет выводиться подборка. Номер должен быть больше 0'
    )
    type_order = models.IntegerField(
        verbose_name='Порядок вывода подборок по типу',
        help_text=
        'Чем выше порядок, тем ниже будет выводиться подборка. Номер должен быть больше 0'
    )
    catalog_order = models.IntegerField(
        verbose_name='Порядок вывода блока для скачивания каталога',
        help_text=
        'Чем выше порядок, тем ниже будет выводиться подборка. Номер должен быть больше 0'
    )

    @classmethod
    def value(self):
        return self.objects.get()

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return 'Настройки. Должны быть одни'
