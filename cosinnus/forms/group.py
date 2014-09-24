# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from awesome_avatar import forms as avatar_forms
from multiform import InvalidArgument

from cosinnus.models.group import (CosinnusGroup, CosinnusGroupMembership,
    MEMBERSHIP_MEMBER)
from django.forms.util import ErrorList


class GroupKwargModelFormMixin(object):
    """
    Generic model form mixin for popping group out of the kwargs and
    attaching it to the instance.

    This mixin must precede ``forms.ModelForm`` / ``forms.Form``. The form is
    not expecting these kwargs to be passed in, so they must be popped off
    before anything else is done.
    """
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group', None)
        super(GroupKwargModelFormMixin, self).__init__(*args, **kwargs)
        if self.group and hasattr(self.instance, 'group_id'):
            self.instance.group_id = self.group.id


class _CosinnusGroupForm(forms.ModelForm):
    
    avatar = avatar_forms.AvatarField(required=False, disable_preview=True)
    
    class Meta:
        fields = ('name', 'public', 'description', 'avatar', 'parent', 'website')
        model = CosinnusGroup
    
    def __init__(self, instance, *args, **kwargs):    
        super(_CosinnusGroupForm, self).__init__(instance=instance, *args, **kwargs)
        
        if instance and instance.type != CosinnusGroup.TYPE_PROJECT:
            del self.fields['parent']
            
            
from cosinnus.forms.tagged import get_form  # circular import


class CosinnusGroupForm(get_form(_CosinnusGroupForm, attachable=False)):

    def dispatch_init_group(self, name, group):
        if name == 'media_tag':
            return group
        return InvalidArgument

    def dispatch_init_user(self, name, user):
        if name == 'media_tag':
            return user
        return InvalidArgument


class MembershipForm(GroupKwargModelFormMixin, forms.ModelForm):

    class Meta:
        fields = ('user', 'status',)
        model = CosinnusGroupMembership

    def __init__(self, *args, **kwargs):
        user_qs = kwargs.pop('user_qs')
        super(MembershipForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = user_qs
        self.initial.setdefault('status', MEMBERSHIP_MEMBER)

    def save(self, *args, **kwargs):
        obj = super(MembershipForm, self).save(commit=False)
        obj.group = self.group
        obj.save()
        return obj
