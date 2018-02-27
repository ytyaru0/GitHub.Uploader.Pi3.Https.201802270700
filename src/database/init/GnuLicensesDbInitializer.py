#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database.init.DbInitializer import DbInitializer
class GnuLicensesDbInitializer(DbInitializer):
    @property
    def DbFileName(self): return 'Gnu.Licenses.sqlite3'

