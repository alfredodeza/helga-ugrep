import re
import random
from helga.plugins import match
from helga.db import db
from helga import log, settings
from helga.plugins import command, match

logger = log.getLogger(__name__)


def store_nick_activity(channel, nick):
    """
    Records a new fact with a given term. Optionally can set an author
    """
    logger.info('Adding new nick activity {0}: {1}'.format(nick, channel))

    #if not db.facts.find({'term': term_regex(term)}).count():
    db.facts.insert({
        'nick': nick,
        'channel': channel,
        'set_date': time.time()
    })
    db.facts.ensure_index('nick')


def find_activity(nick):
    record = db.facts.find_one({'nick': nick})

    if record is None:
        return 'hrmnnn have not seen {nick} around at all'.format(nick=nick)

    return 'last saw {nick} on {date}'.format(nick=nick, date=record['set_date'])
    # Otherwise, do normal formatting
    #tz = getattr(settings, 'TIMEZONE', 'US/Eastern')
    #try:
    #    timestamp = datetime.fromtimestamp(record['set_date'], tz=pytz.timezone(tz))
    #except TypeError:
    #    timestamp = record['set_date'].replace(tzinfo=pytz.timezone(tz))
    #record['fmt_dt'] = datetime.strftime(timestamp, '%m/%d/%Y %I:%M%p')

    #return '{fact} ({set_by} on {fmt_dt})'.format(**record)


@command('ugrep', help="grep for a user's last activity. Usage: <botnick> ugrep nick")
@match(r'^(.*)\?$')  # Capture every line
def ugrep(client, channel, nick, message, *args):
    if len(args) == 2:
        return find_activity(args[-1])

    # Anything else is a match
    store_nick_activity(channel, nick)
