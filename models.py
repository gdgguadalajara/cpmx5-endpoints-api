from google.appengine.ext import ndb

class Coordinate(ndb.Model):
    user = ndb.StringProperty(required=True)
    geo_pos = ndb.GeoPtProperty(required=True)
    date_time = ndb.StringProperty(required=True)




