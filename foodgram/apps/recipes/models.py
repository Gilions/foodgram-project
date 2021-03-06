from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from .services import translate_rus_eng

User = get_user_model()


class Composition(models.Model):
    # Таблица компонентов
    name = models.CharField(
        db_index=True,
        max_length=100,
        unique=True,
        verbose_name='Название ингредиента',
        help_text='Название ингредиента, максимум 100 символов'
    )
    unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения',
        help_text='Единица измерения, максимум 20 симоволов'
    )

    class Meta:
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='Тег',
        help_text='Тег рецепта, максимум 20 символов',
    )
    display_name = models.CharField(
        max_length=50,
        verbose_name='Название тега для HTML',
        blank=True
    )
    color = models.CharField(
        max_length=20,
        verbose_name='Цвет тега',
        blank=True
    )

    class Meta:
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.display_name


class Recipe(models.Model):
    # Основаная таблица, книга рецептов
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        )
    name = models.CharField(
        max_length=100,
        verbose_name='Название рецепта',
        help_text='Максимальная длинна 100 символов',
        )
    image = models.ImageField(
        upload_to='recipes/',
        help_text='Изображение',
        verbose_name='Изображение',
        )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Описание рецепта',
        )
    ingredients = models.ManyToManyField(
        Composition,
        through='Amount',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Игредиенты',
        help_text='Игредиенты',
    )
    time_cooking = models.PositiveSmallIntegerField(
        verbose_name='Вермя приготовления'
        )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата публикации',
        )
    fav_counter = models.PositiveSmallIntegerField(
        verbose_name='Добавление в избранное',
        help_text='Количество добавлений в избранное',
        default=0,
        )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        help_text='Тег рецепта',
    )
    slug = models.SlugField(
        max_length=500,
        unique=True,
        blank=True,
        )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name_plural = "Рецепты"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = translate_rus_eng(self.name) + '_' + datetime.strftime(
                timezone.now(), '%d_%m_%y_%H_%M_%S_%s'
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Amount(models.Model):
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        validators=[MinValueValidator(1)]
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
        help_text='Рецепт'
    )
    ingredient = models.ForeignKey(
        Composition,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Ингредиент',
        help_text='Ингредиент'
    )

    class Meta:
        verbose_name_plural = "Состав"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
    )

    class Meta:
        verbose_name_plural = "Избранные"


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_subscription')
            ]
        verbose_name_plural = "Подписка"


class Cart(models.Model):
    item = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['item', 'customer'],
                                    name='unique_purchase')
        ]
        verbose_name_plural = "Корзина"
