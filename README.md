# YUMROAD-APP
- based off of https://gumroad.com (create and edit products)

### Notes
- export FLASK_APP=yumroad:create_app
- export FLASK_ENV=development
- flask shell
- run 'pytest --cov=yumroad --cov-report term-missing' on terminal to test
- set all environmental variables when testing

### ToDo
- Mailgun testing coverage
- Update Mailgun plan to be able to send emails to not use myself (use AWS?)