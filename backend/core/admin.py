from django.contrib import admin
from core.models import KPGZ, OKEI, OKPD, OKPD2, FileUpdate, SPGZ, SN, SNSection, SNSubsection, SNRow, SNSubRow, TZ, TZRow

admin.site.register(KPGZ)
admin.site.register(OKEI)
admin.site.register(OKPD)
admin.site.register(OKPD2)
admin.site.register(FileUpdate)
admin.site.register(SPGZ)
admin.site.register(SN)
admin.site.register(SNSection)
admin.site.register(SNSubsection)
admin.site.register(SNRow)
admin.site.register(SNSubRow)
admin.site.register(TZ)
admin.site.register(TZRow)