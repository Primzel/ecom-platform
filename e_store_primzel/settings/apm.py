import os

ELASTIC_APM = {
    # Set required service name. Allowed characters:
    # a-z, A-Z, 0-9, -, _, and space
    'SERVICE_NAME': os.getenv('SERVICE_NAME','store'),

    # Use if APM Server requires a token
    'SECRET_TOKEN': os.getenv('SECRET_TOKEN',''),

    # Set custom APM Server URL (default: http://localhost:8200)
    'SERVER_URL': os.getenv('SERVER_URL','http://com.primzel.apm:8200'),
    'DEBUG': True,
}