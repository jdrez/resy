import helpers.config
import helpers.datetime
import helpers.firebase
import helpers.logger
import helpers.resy

import datetime
import pytz
import re

log = helpers.logger.Logger(__name__)


def run(event={}, context={}):
    helpers.config.refresh()
    email = helpers.config.get('resy.email')
    password = helpers.config.get('resy.password')
    log.info("email", email=email, password=re.sub(r".", "*", password))

    reserve = helpers.firebase.reserve()
    if len(reserve) == 0:
        log.warn("no reservations to make")
        return

    helpers.resy.login(email, password)
    log.info("user", user=helpers.resy.USER)

    for d in reserve:
        print("——————————")
        r = d.to_dict()

        venue_id = r['venue_id']
        party_size = r['party_size']
        date = helpers.datetime.parse_firebase(r['date'])
        log.info("resy", venue_id=venue_id, party_size=party_size, date=date)

        if helpers.datetime.missed(date):
            log.warn("this resy was missed")
            helpers.firebase.missed(d.id, r)
            continue

        venues = helpers.resy.find(date, venue_id, party_size)
        if len(venues) == 0:
            log.warn("no venue found for resy")
            continue
        if len(venues) > 1:
            log.warn("too many venues found for resy")

        slots = venues[0]['slots']
        slot = next(iter(s for s in slots if s['date']['start'] == helpers.datetime.datetime_resy(date)), None)
        log.info("slot", slot=slot)
        if slot == None:
            log.warn("no slot found for resy")
            continue

        config_token = slot['config']['token']
        log.info("config_token", config_token=config_token)

        details = helpers.resy.details(config_token, date, party_size)
        book_token = details['book_token']['value']
        log.info("book_token", book_token=book_token)

        booked = helpers.resy.book(book_token)
        log.info("booked", booked=booked)
        r['booked'] = booked
        helpers.firebase.booked(d.id, r)

    log.info("done")

if __name__ == '__main__':
    run();
