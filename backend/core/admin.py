from django.contrib import admin
from core.models import (KPGZ, OKEI, OKPD, OKPD2, FileUpdate, SPGZ, 
                            SN, SNSection, SNRow, SNSubRow, 
                            TZ, TZRow,
                            Smeta, SmetaSection, SmetaSubsection, SmetaRow, SmetaSubRow)

admin.site.register(KPGZ)
admin.site.register(OKEI)
admin.site.register(OKPD)
admin.site.register(OKPD2)
admin.site.register(FileUpdate)
admin.site.register(SPGZ)
admin.site.register(SN)
admin.site.register(SNSection)
admin.site.register(SNRow)
admin.site.register(SNSubRow)
admin.site.register(Smeta)
admin.site.register(SmetaSection)
admin.site.register(SmetaSubsection)
admin.site.register(SmetaRow)
admin.site.register(SmetaSubRow)
admin.site.register(TZ)
admin.site.register(TZRow)