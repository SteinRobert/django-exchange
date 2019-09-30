# Django Exchange

Simple `EmailBackend` for Django to interact with Microsoft
Exchange Servers. 

## Configuration

Standard configuration - there is only one new setting: `EMAIL_DOMAIN`.

```python
EMAIL_HOST = 'mail.example.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'user-name'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_DOMAIN = 'domain.example.com'  # This is the only new setting.
```

