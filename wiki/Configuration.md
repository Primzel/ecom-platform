
# Configuration
1. **Set environment variables**:
   ```bash
   export PYTHONUNBUFFERED=1
   export DJANGO_SETTINGS_MODULE=e_store_primzel.settings
   export POSTGRES_HOST=localhost
   export PRIMZEL_DEBUG=True
   ```

2. **Configure local settings**:
   Add the following parameters in `/web-backend/e_store_primzel/settings/env/local.py`:
   ```python
   THUMBNAIL_DEBUG = True
   THUMBNAIL_PRESERVE_FORMAT = True
   ```
