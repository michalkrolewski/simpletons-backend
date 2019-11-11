def isPublic(category):
    return category.user_id is not None


def fillFiszkiWithCategoryId(fiszki, xid):
    for fiszka in fiszki:
        fiszka.category_id = xid
