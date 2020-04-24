import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'checkout_file': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'error_file': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
        'logstash': {
            'level': 'DEBUG',
            'class': 'logstash.TCPLogstashHandler',
            'host': os.getenv('LOGSTASH_HOST','com.primzel.elk'),   # IP/name of our Logstash EC2 instance
            'port': os.getenv('LOGSTASH_TCP_INPUT_PORT',5959),
            'version': 1,
            'message_type': 'logstash',
            'fqdn': True,
            'tags': ['store'],
        }
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} {module} {levelname} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'loggers': {
        'template_loader': {
            'handlers': ['console','logstash'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'oscar': {
            'handlers': ['console','logstash'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'oscar.checkout': {
            'handlers': ['console','logstash'],
            'propagate': True,
            'level': 'INFO',
        },
        'datacash': {
            'handlers': ['console','logstash'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'primzel.requests': {
            'handlers': ['console','logstash'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'primzel.logger': {
            'handlers': ['console','logstash'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
