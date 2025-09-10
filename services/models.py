from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class TransportType(models.Model):
    title = models.CharField(max_length=255)
    is_popular = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class TransportBrand(models.Model):
    title = models.CharField(max_length=255)
    is_popular = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class TransportModel(models.Model):
    title = models.CharField(max_length=255)
    is_popular = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Characteristic(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class CharacteristicValue(models.Model):
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE)
    value = models.IntegerField()
    title = models.CharField(max_length=255)
    measurement_unit = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.value}{self.measurement_unit or ''})"


class Price(models.Model):
    TYPE_CHOICES = (
        ('price', 'Fixed Price'),
        ('negotiable', 'Negotiable'),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='uzs')

    def __str__(self):
        return f"{self.price} {self.currency} ({self.get_type_display()})"


class Image(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url


# ---- Abstract base service ----
class BaseService(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    address = models.CharField(max_length=255, blank=True)
    prices = models.ManyToManyField("Price", blank=True)
    images = models.ManyToManyField("Image", blank=True)
    transport_type = models.ForeignKey("TransportType", on_delete=models.SET_NULL, null=True, blank=True)
    transport_brand = models.ForeignKey("TransportBrand", on_delete=models.SET_NULL, null=True, blank=True)
    transport_model = models.ForeignKey("TransportModel", on_delete=models.SET_NULL, null=True, blank=True)
    characteristics = models.ManyToManyField("CharacteristicValue", blank=True)
    rank_premium = models.BooleanField(default=False)
    rank_search = models.BooleanField(default=False)
    rank_hot_offer = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    phones = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default='pending')  # confirmed, cancelled, etc.
    is_negotiable = models.BooleanField(default=False)
    stickers = models.JSONField(default=list, blank=True)
    statistics = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def increment_view(self):
        self.statistics['viewed'] = self.statistics.get('viewed', 0) + 1
        self.save()

    def toggle_like(self, user):
        if user.favorites.filter(id=self.id).exists():
            user.favorites.remove(self)
            self.statistics['favorite'] = max(0, self.statistics.get('favorite', 0) - 1)
        else:
            user.favorites.add(self)
            self.statistics['favorite'] = self.statistics.get('favorite', 0) + 1
        self.save()

    def __str__(self):
        return self.title


# ---- Child models ----
class Product(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Equipment(BaseService):
    author = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="equipments")

    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"

    def __str__(self):
        return f"Equipment: {self.title}"


class News(BaseService):
    author = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="news")
    publish_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return f"News: {self.title}"


class HotOffer(BaseService):
    author = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="hot_offers")

    class Meta:
        verbose_name = "Hot Offer"
        verbose_name_plural = "Hot Offers"

    def __str__(self):
        return f"Hot Offer: {self.title}"


class Ad(BaseService):
    author = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="ads")
    duration_days = models.PositiveIntegerField(default=30)  # E'lon necha kun aktiv bo'lishi
    is_featured = models.BooleanField(default=False)         # Tanlangan e'lon

    class Meta:
        verbose_name = "Ad"
        verbose_name_plural = "Ads"

    def __str__(self):
        return self.title
