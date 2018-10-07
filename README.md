## Friendly Mail

This shell script automatically sends emails to friends. On birthdays and every four months. This program runs in linux and requires to setup ssmtp. To run this script periodically, you can use anacron.

### Required User Input

#### Add friends data
Create a `people.csv` file with the following format
```
Name, Email, Birthday
Firstname Lastname,email@provider.com,dd.mm.yyyy
```
#### Add birthday text
Create a `birthday_template.txt`. You can use $NAME and $AGE variables, which will
be replaced by the script with your friend's data
```
Dear $NAME,

Happy Birthday! You are $AGE!

Yours,
Friendly Mail
```
#### Add reconnection text
Create a `recon_template.txt`. You can use $NAME and $AGE variables, which will
be replaced by the script with your friend's data
```
Dear $NAME,

It's been a long time. How are you?

Yours,
Friendly Mail
```

### Script Generated data

#### meta.dat
This file holds the date of the last run.

#### history.log
Log of the last runs
