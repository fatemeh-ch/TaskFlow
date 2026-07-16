from django import template
import jdatetime

register = template.Library()


@register.filter
def jalali(value):
    """
        Convert date to Jalali date
    """
    if not value:
        return ""

    j_date = jdatetime.datetime.fromgregorian(datetime=value)
    return j_date.strftime("%A %d %B %Y - %H:%M")