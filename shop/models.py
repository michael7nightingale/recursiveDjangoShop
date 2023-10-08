from django.db import models


class CategoryManager(models.Manager):

    def get_super_categories(self, id):
        return Category.objects.raw(
            f"""WITH RECURSIVE category AS (
                          SELECT shop_category.id, shop_category.name, shop_category.category_id, 1 as depth
                          FROM shop_category
                          WHERE shop_category.id = {id}
                        UNION ALL
                          SELECT sc.id AS id, sc.name AS name, sc.category_id as category_id, depth + 1 as depth
                          FROM shop_category as sc, category as c
                          WHERE sc.id = c.category_id
                        )
                        SELECT * FROM category
                        ORDER BY depth
                    """)

    def get_subcategories(self, id):
        return Category.objects.raw(
            f"""WITH RECURSIVE category AS (
                          SELECT shop_category.id, shop_category.name, shop_category.category_id, 1 as depth
                          FROM shop_category
                          WHERE shop_category.id = {id}
                        UNION ALL
                          SELECT sc.id AS id, sc.name AS name, sc.category_id as category_id, depth + 1 as depth
                          FROM shop_category as sc, category as c
                          WHERE sc.category_id = c.id
                        )
                        SELECT * FROM category
                        WHERE id != {id}
                        ORDER BY depth
                    """)


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")

    objects = CategoryManager()

    def __str__(self):
        return self.name


class Good(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
