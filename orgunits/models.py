"""
Copyright 2020 ООО «Верме»
"""

from django.db import models
from django.db.models.expressions import RawSQL


class OrganizationQuerySet(models.QuerySet):
    def tree_downwards(self, root_org_id):
        """
        Возвращает корневую организацию с запрашиваемым root_org_id и всех её детей любого уровня вложенности

        :type root_org_id: int
        """
        result = self.filter(id=root_org_id)
        if not result:
            return result

        root = result.first()
        children = root.organization_set.all()
        if children is None:
            return result

        for child in children:
            result = result | self.tree_downwards(child.id)

        return result

    def tree_upwards(self, child_org_id):
        """
        Возвращает корневую организацию с запрашиваемым child_org_id и всех её родителей любого уровня вложенности
        TODO: Написать фильтр с помощью ORM или RawSQL запроса или функций Python

        :type child_org_id: int
        """
        result = self.filter(id=child_org_id)
        if not result:
            return result

        child = result.first()
        while parent := child.parent:
            result = result | self.filter(id=parent.id)
            child = parent

        return result



class Organization(models.Model):
    """ Организаци """

    objects = OrganizationQuerySet.as_manager()

    name = models.CharField(max_length=1000, blank=False, null=False, verbose_name="Название")
    code = models.CharField(max_length=1000, blank=False, null=False, unique=True, verbose_name="Код")
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, verbose_name="Вышестоящая организация",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Организация"
        verbose_name = "Организации"

    def parents(self):
        """
        Возвращает всех родителей любого уровня вложенности
        TODO: Написать метод, используя ORM и .tree_upwards()

        :rtype: django.db.models.QuerySet
        """
        result = Organization.objects.tree_upwards(self.id)
        return result.exclude(id=self.id)

    def children(self):
        """
        Возвращает всех детей любого уровня вложенности

        :rtype: django.db.models.QuerySet
        """
        result = Organization.objects.tree_downwards(self.id)
        return result.exclude(id=self.id)

    def __str__(self):
        return self.name
