# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from haystack import indexes

from cosinnus.models.group import CosinnusGroup
from cosinnus.utils.search import TagObjectSearchIndex, TemplateResolveCharField,\
    TemplateResolveEdgeNgramField


class GroupIndex(TagObjectSearchIndex, indexes.Indexable):
    text = TemplateResolveEdgeNgramField(document=True, use_template=True)
    rendered = TemplateResolveCharField(use_template=True, indexed=False)

    name = indexes.CharField(model_attr='name', boost=1.25)
    slug = indexes.CharField(model_attr='slug', indexed=False)
    public = indexes.BooleanField(model_attr='public')
    admins = indexes.MultiValueField(model_attr='admins', indexed=False)
    members = indexes.MultiValueField(model_attr='members', indexed=False)
    pendings = indexes.MultiValueField(model_attr='pendings', indexed=False)

    def get_model(self):
        return CosinnusGroup

    def index_queryset(self, using=None):
        qs = self.get_model().objects.all()
        qs = qs.filter(group__is_active=True)
        qs = qs.select_related('media_tag').all()
        return qs
