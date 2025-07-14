from celery.schedules import crontab
from cron_validator import CronValidator
from pydantic import AfterValidator
from typing import Annotated


def validate_cron_expression(cron_expression: str):
    if not CronValidator.parse(cron_expression):
        raise ValueError(f'{cron_expression} is not a valid cron expression')
    return crontab(minute=cron_expression.split(' ')[0],
                   hour=cron_expression.split(' ')[1],
                   day_of_month=cron_expression.split(' ')[2],
                   month_of_year=cron_expression.split(' ')[3],
                   day_of_week=cron_expression.split(' ')[4])


CronExpression = Annotated[str, AfterValidator(validate_cron_expression)]
