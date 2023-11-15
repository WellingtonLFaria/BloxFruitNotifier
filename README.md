# 🍈 Blox Fruit Notifier 🍈

Blox Fruit Notifier is an application where the user selects the desired fruits from the Blox Fruits game store, and when the desired fruits are in stock in the game store, the application notifies the user that the fruit is in stock via the email configured by the user.

# Preparing the application

## Creating .env file and configuring variables

To have the send notification functionality working, you need to configure the email address that will send the notification and your password in the .env file.
Variables:
```
FROM_EMAIL = "notification@email.com"
FROM_EMAIL_PASSWORD = "notification_email_password"
```

## Installing dependencies

```bash
pip install -r requirements.txt
```

# Running the application

```bash
python main.py
```
