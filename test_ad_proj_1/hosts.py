from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'', settings.ROOT_URLCONF, name='front'),  # <-- The `name` we used to in the `DEFAULT_HOST` setting
    host(r'admin', 'user_admin.urls', name='user_admin'),
    host(r'accountant', 'accountant.urls', name='accountant'),
    host(r'marketer', 'marketer.urls', name='marketer'),
    host(r'publisher', 'publisher.urls', name='publisher'),
)
