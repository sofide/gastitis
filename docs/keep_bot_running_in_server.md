# Keep bot runnin in server

This is a guide to  use supervisorctl to keep the bot running.

## 1. Install supervisorctl

Run the following command to install Supervisor:

```bash
sudo apt update
sudo apt install supervisor
```

## 2. Create a Configuration File for Your Program
Supervisor configuration files are typically stored in /etc/supervisor/conf.d/. 
Create a new configuration file for your program, e.g., gastitis.conf:

```bash
sudo nano /etc/supervisor/conf.d/gastitis.conf
```

## 3. Add Configuration for Your Program
Add the following content to the configuration file, replacing placeholders with your program's details:

```
[program:gastitis]
command=</path/to/your/venv>/bin/python manage.py startbot
directory=<path/to_your_repo>
autostart=true                 # Start the program when Supervisor starts
autorestart=true               # Restart the program if it exits unexpectedly
stderr_logfile=/var/log/gastitis.err.log  # Log for standard error
stdout_logfile=/var/log/gastitis.out.log  # Log for standard output
user=<username>                  # The user under which to run the program
```
## 4. Update Supervisor Configuration
After saving the configuration file, update Supervisor to recognize the new program:

```bash
sudo supervisorctl reread
sudo supervisorctl update
```

## 5. Start and Monitor Your Program
Start your program using Supervisor:

```bash
sudo supervisorctl start gastitis
```

You can check the program's status with:

```bash
sudo supervisorctl status
```

## 6. View Logs
To debug or monitor the program's output, view the logs:

```bash
tail -f /var/log/gastitis.out.log
tail -f /var/log/gastitis.err.log
```
