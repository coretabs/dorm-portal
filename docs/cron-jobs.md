# cron Jobs

## What is cron?

cron is a time-based job scheduler in Unix-like computer operating systems.

## What are the scheduled jobs?

There are two schedule jobs:

1. Update exchange rates (for currency conversion).
2. Collect quotas from non-finished reservations (efficient way to ensure non-paid reservations are cleaned up).

## Configure cron jobs

The [`Dockerfile`](https://github.com/coretabs/dorm-portal/blob/master/Dockerfile) contains the cron job configuration for both jobs:

```
RUN crontab -l | { cat; echo "0 */2 * * * cd /dormportal/app; python manage.py collectquota && python manage.py update_rates"; } | crontab -
```

The `0 */2 * * *` means that it will run every two hours, you can use this website if you wish to change this value:

[https://crontab.guru](https://crontab.guru/#0_*/2_*_*_*)