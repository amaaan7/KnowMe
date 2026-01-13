import os
from decouple import config

# Database credentials
db_user = config('DB_USER', default=None)
db_password = config('DB_PASS', default=None)

# Email credentials
email_user = config('EMAIL_USER', default=None)
email_pass = config('EMAIL_PASS', default=None)

print("DB_USER:", db_user)
print("DB_PASS:", db_password)
print("EMAIL_USER:", email_user)
print("EMAIL_PASS:", email_pass)