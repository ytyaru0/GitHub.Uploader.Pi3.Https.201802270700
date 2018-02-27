import ApisDbInitializer
import GnuLicensesDbInitializer
for dbiniter in [ApisDbInitializer.ApisDbInitializer(), GnuLicensesDbInitializer.GnuLicensesDbInitializer()]:
    dbiniter.CreateDb()
    print(dbiniter.DbId)
    print(dbiniter.DbFileName)
    dbiniter.CreateTable()
