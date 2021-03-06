# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.core.urlresolvers import reverse
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.utils.http import urlquote


DEFAULT_CONTENT_MODELS = [
    'cosinnus_note.Note', 
    'cosinnus_file.FileEntry',
    'cosinnus_event.Event',
    'cosinnus_poll.Poll',
    'cosinnus_marketplace.Offer',
    'cosinnus_todo.TodoEntry',
    'cosinnus_etherpad.Etherpad'
]

def move_group_content(from_group, to_group, models=None, verbose=False):
    """ Moves all BaseTaggableObject content from one CosinnusGroup to another. """
    if not models:
        models = DEFAULT_CONTENT_MODELS
    
    actions_done = []
    for model_str in models:
        app_label, model = model_str.split('.')
        model_cls = get_model(app_label, model)
        for obj in model_cls.objects.filter(group=from_group):
            obj.group = to_group
            obj.save()
            s = "moved '%d' %s: from group %d to group %d" % (obj.id, model_str, from_group.id, to_group.id)
            if verbose:
                print(s)
            actions_done.append(s)
    return actions_done


_CosinnusGroup = None

def get_cosinnus_group_model():
    """
    Return the cosinnus tag object model that is defined in
    :data:`settings.COSINNUS_TAG_OBJECT_MODEL`
    
    Also we cache the CosinnusGroupModel to save calling django internals forever.
    """
    global _CosinnusGroup
    if _CosinnusGroup is None:
        from django.core.exceptions import ImproperlyConfigured
        #from django.db.models import get_model
        from django.apps import apps
        from cosinnus.conf import settings
    
        try:
            app_label, model_name = settings.COSINNUS_GROUP_OBJECT_MODEL.split('.')
        except ValueError:
            raise ImproperlyConfigured("COSINNUS_GROUP_OBJECT_MODEL must be of the form 'app_label.model_name'")
        #tag_model = get_model(app_label, model_name)
        group_model = apps.get_model(app_label=app_label, model_name=model_name)
        if group_model is None:
            raise ImproperlyConfigured("COSINNUS_GROUP_OBJECT_MODEL refers to model '%s' that has not been installed" %
                settings.COSINNUS_TAG_OBJECT_MODEL)
        _CosinnusGroup = group_model
        
    return _CosinnusGroup   


def message_group_admins_url(group, group_admins=None):
    """ Generates a postman:write URL to the admins of the given group, complete with subject line """
    group_admins = group_admins or group.actual_admins
    if not group_admins:
        return None
    message_subject = force_text(_('Question about')) + ' ' + force_text(_('Group') if group.type == group.TYPE_SOCIETY else _('Project')) + ': ' + group.name
    return reverse('postman:write', kwargs={'recipients':','.join([user.username for user in group_admins])}) + '?subject=' + urlquote(message_subject)
        
