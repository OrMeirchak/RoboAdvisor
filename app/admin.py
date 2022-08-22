from django.contrib import admin
from .models import Algorithm, Algotrade_index, Algotrade_type, Question,Answer

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Algorithm)
admin.site.register(Algotrade_type)
admin.site.register(Algotrade_index)