from django.contrib import admin
from .models import userInformation,eslesme,danisan,antrenor,danisan_kayitlari,egzersiz_beslenme_planlari,plan_eslesme

admin.site.register(userInformation)
admin.site.register(eslesme)
admin.site.register(danisan)
admin.site.register(antrenor)
admin.site.register(danisan_kayitlari)
admin.site.register(egzersiz_beslenme_planlari)
admin.site.register(plan_eslesme)


