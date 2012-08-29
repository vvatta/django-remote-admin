from django.contrib.admin.sites import site
from django.core.serializers.json import simplejson as json
from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import Http404, HttpResponse
from django.utils.text import capfirst


def handle_login(request):
    if request.method == 'GET':
        # Return login form
        pass
    elif request.method == 'POST':
        # Process login
        pass


def get_models(request, app_label=None):
    # Return data on all models registered with admin
    user = request.user

    if app_label is None:
        if user.is_staff or user.is_superuser:
            has_module_perms = True
    else:
        has_module_perms = user.has_module_perms(app_label)

    app_dict = {}
    for model, model_admin in site._registry.items():
        model_name = model._meta.module_name

        if app_label is not None and app_label != model._meta.app_label:
            continue
        else:
            app_label = model._meta.app_label

        if has_module_perms:
            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True in perms.values():
                model_dict = {
                    'name': unicode(capfirst(model._meta.verbose_name_plural)),
                    'perms': perms,
                }
                if perms.get('change', False):
                    try:
                        model_dict['admin_url'] = reverse('adminapi_view_models', args=[app_label])
                    except NoReverseMatch:
                        pass
                if perms.get('add', False):
                    try:
                        model_dict['add_url'] = reverse('adminapi_handle_instance_form', args=[app_label, model_name])
                    except NoReverseMatch:
                        pass
                if app_dict:
                    app_dict['models'].append(model_dict),
                else:
                    # First time around, now that we know there's
                    # something to display, add in the necessary meta
                    # information.
                    app_dict = {
                        'name': app_label.title(),
                        'app_url': '',
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                    }
    if not app_dict:
        raise Http404('The requested admin page does not exist.')

    # Sort the models alphabetically within each app.
    app_dict['models'].sort(key=lambda x: x['name'])
    response_data = {
        'title': '%s administration' % capfirst(app_label),
        'app_list': [app_dict],
    }

    return HttpResponse(json.dumps(response_data), mimetype="application/json")


def get_model_instances(request, model_name):
    # Return list of instances for a given model
    pass


def handle_instance_form(request, model_name, instance_id):
    if request.method == 'GET':
        # Return instance form for given model name
        # Return initial values if instance ID is supplied, otherwise return empty form
        pass
    elif request.method == 'POST':
        # Create new instance for given data
        pass
    elif hasattr(request, 'raw_post_data'):
        # PUT data available, update instance
        pass