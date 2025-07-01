# Mailer
You can send email messages automatically using this project.

## Settings
1. Turn on two-factor authentification in your Google account.
2. Go to https://myaccount.google.com/apppasswords and create new App Password with any app name you want.
3. Create your `.env` file:
    ```
    SENDER_EMAIL=your@gmail.com
    SENDER_APP_PASSWORD=your_app_password_without_spaces
    ```
4. Create your `people.csv`:
   ```
   Email,FirstName,LastName,Affiliation
   ...
   ```
5. Create your `subject.txt` and `body.md`
