import re
import random
import time
from helga.plugins import match
from helga.db import db
from helga import log, settings
from helga.plugins import command, match, preprocessor

logger = log.getLogger(__name__)


def store_nick_activity(channel, nick):
    """
    Records a new fact with a given term. Optionally can set an author
    """
    logger.info('Adding new nick activity {0}: {1}'.format(nick, channel))
    db.ugrep.remove({'nick': nick})

    #if not db.facts.find({'term': term_regex(term)}).count():
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

    return 'last saw {nick} on channel: {channel} at {date}'.format(
            nick=nick, channel=record['channel'], date=record['set_date'])

@preprocessor(priority=50)
@command('ugrep', help="grep for a user's last activity. Usage: <botnick> ugrep nick")
#@match(r'(.*)', priority=50)
def ugrep(client, channel, nick, message, *args):
    if len(args) == 0:
        is_asking = bool(re.findall(r'(ugrep)\s+{0}$'.format(client.nickname)))

        if is asking
            return channel, nick, message

    if len(args) == 2:
        return find_activity(args[-1][0])

    # Anything else is a match
    return store_nick_activity(channel, nick)
