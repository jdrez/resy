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

        location = r['location']
        slug = r['slug']
        party_size = r['party_size']
        date = helpers.datetime.parse_firebase(r['date'])
        log.info("resy", location=location, slug=slug, party_size=party_size, date=date)

        if helpers.datetime.missed(date):
            log.error("resy date was missed")
            helpers.firebase.missed(d.id, r)
            continue

        venue_id = helpers.resy.venue(location, slug)
        log.info("venue_id", venue_id=venue_id)
        if venue_id is None:
            log.error("no venue_id found for resy")
            continue

        venues = helpers.resy.find(date, venue_id, party_size)
        if len(venues) == 0:
            log.error("no venue found for resy")
            continue
        if len(venues) > 1:
            log.warn("too many venues found for resy")

        slots = venues[0]['slots']
        log.info("slots", slots=slots)
        valid_slots = helpers.resy.valid_slots(date, slots)
        log.info("valid_slots", valid_slots=valid_slots)

        if len(valid_slots) == 0:
            log.warn("no slot found for resy")
            continue

        slot = valid_slots[0]
        log.info("slot", slot=slot)

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
    return True

if __name__ == '__main__':
    run();
