import re
import time
import datetime
from helga.plugins import match
from helga.db import db
from helga import log
from helga.plugins import command, match, preprocessor

logger = log.getLogger(__name__)


def store_nick_activity(channel, nick):
    """
    Records a new fact with a given term. Optionally can set an author
    """
    logger.info('Adding new nick activity {0}: {1}'.format(nick, channel))
    db.ugrep.remove({'nick': nick})

    db.ugrep.insert({
        'nick': nick,
        'channel': channel,
        'set_date': time.time()
    })
    db.ugrep.ensure_index('nick')


def find_activity(nick):
    record = db.ugrep.find_one({'nick': nick})

    if record is None:
        return 'hrmnnn have not seen {nick} around at all'.format(nick=nick)

    record_date = datetime.datetime.fromtimestamp(record['set_date'])
    last_saw = timesince(record_date)
    return 'last saw {nick} {ago} ago on channel: {channel}'.format(
        nick=nick, channel=record['channel'], ago=last_saw)


@preprocessor(priority=50)
@command('ugrep', help="grep for a user's last activity. Usage: <botnick> ugrep nick")
def ugrep(client, channel, nick, message, *args):
    if len(args) == 0:
        is_asking = bool(re.findall(r'(ugrep)\s+{0}$'.format(client.nickname), message))
        if is_asking:
            return channel, nick, ''

    if len(args) == 2:
        return find_activity(args[-1][0])

    # Anything else is a match
    else:
        store_nick_activity(channel, nick)

    return channel, nick, message

#
# Relative Times
#


def ungettext(a, b, count):
    if count:
        return b
    return a


def ugettext(a):
    return a


def timesince(d, now=None):
    """
    Takes two datetime objects and returns the time between d and now
    as a nicely formatted string, e.g. "10 minutes".  If d occurs after now,
    then "0 minutes" is returned.

    Units used are years, months, weeks, days, hours, and minutes.
    Seconds and microseconds are ignored.  Up to two adjacent units will be
    displayed.  For example, "2 weeks, 3 days" and "1 year, 3 months" are
    possible outputs, but "2 weeks, 3 hours" and "1 year, 5 days" are not.

    Adapted from http://blog.natbat.co.uk/archive/2003/Jun/14/time_since
    """
    chunks = (
      (60 * 60 * 24 * 365, lambda n: ungettext('year', 'years', n)),
      (60 * 60 * 24 * 30, lambda n: ungettext('month', 'months', n)),
      (60 * 60 * 24 * 7, lambda n : ungettext('week', 'weeks', n)),
      (60 * 60 * 24, lambda n : ungettext('day', 'days', n)),
      (60 * 60, lambda n: ungettext('hour', 'hours', n)),
      (60, lambda n: ungettext('minute', 'minutes', n))
    )
    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    if not now:
        now = datetime.datetime.now()

    # ignore microsecond part of 'd' since we removed it from 'now'
    delta = now - (d - datetime.timedelta(0, 0, d.microsecond))
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since <= 0:
        # d is in the future compared to now, stop processing.
        return u'0 ' + ugettext('minutes')
    for i, (seconds, name) in enumerate(chunks):
        count = since // seconds
        if count != 0:
            break
    s = ugettext('%(number)d %(type)s') % {'number': count, 'type': name(count)}
    if i + 1 < len(chunks):
        # Now get the second item
        seconds2, name2 = chunks[i + 1]
        count2 = (since - (seconds * count)) // seconds2
        if count2 != 0:
            s += ugettext(', %(number)d %(type)s') % {'number': count2, 'type': name2(count2)}
    return s

