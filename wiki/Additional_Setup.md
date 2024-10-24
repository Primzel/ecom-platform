
# Additional Setup
1. **Set up SSL**:
   Follow the instructions [here](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal) to set up SSL.

2. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

3. **Integrate with Stripe CLI**:
   Replace `<paste-api-key-here>` with your actual Stripe API key.
   ```bash
   docker run --rm -it stripe/stripe-cli listen --load-from-webhooks-api --forward-to 192.168.1.4:8000 --api-key <paste-api-key-here>
   docker run --rm -it stripe/stripe-cli logs tail --api-key <paste-api-key-here>
   docker run --rm -it stripe/stripe-cli trigger charge.succeeded --api-key <paste-api-key-here>
   ```

4. **Install AWS CLI and create S3 bucket**:
   ```bash
   curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
   unzip awscli-bundle.zip
   sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws
   aws --endpoint-url=http://localhost:4566 s3 mb s3://demo-bucket
   ```
