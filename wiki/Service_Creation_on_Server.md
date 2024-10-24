
# Service Creation on Server
1. **Add `store.oscar.com` to `/etc/hosts`**.
2. **Create a systemd service file**: `/etc/systemd/system/primzel-backend.service`.
3. **Populate the file with the following configuration, replacing sensitive data with your actual credentials**:
   ```shell
   [Unit]
   Description=Primzel backend.

   [Service]
   # Environment variables with masked sensitive data
   Environment="POSTGRES_PASSWORD=********"
   Environment="AWS_ACCESS_KEY_ID=********"
   Environment="AWS_SECRET_ACCESS_KEY=********"
   # Additional configurations...
   ```
