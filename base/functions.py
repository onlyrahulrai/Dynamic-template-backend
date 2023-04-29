from django.conf import settings

def get_templates_directory():
    for engine in settings.TEMPLATES:
        if 'DIRS' in engine:
            return engine['DIRS'][0]
    raise Exception('Templates directory not found in settings')