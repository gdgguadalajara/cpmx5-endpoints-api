import endpoints

from protorpc import messages
from protorpc import message_types
from protorpc import remote
from google.appengine.ext import ndb
from models import Coordinate

package = 'coords'

class CoordinateMessage(messages.Message):
    """Representa el request que requiero en un metodo"""
    id_usuario = messages.StringField(1, required=True)
    latitud = messages.FloatField(2, required=True)
    longitud = messages.FloatField(3, required=True)
    fecha_hora = messages.StringField(4, required=True)


class ResponseMessage(messages.Message):
    value = messages.StringField(1)


class CoordinatesMessage(messages.Message):
    items = messages.MessageField(CoordinateMessage, 1, repeated=True)


class QueryCoordMessage(messages.Message):
    id_usuario = messages.StringField(1, required=True)
    desplazamiento = messages.FloatField(2, required=True)
    cantidad = messages.IntegerField(3, required=True)


@endpoints.api(name='coordinates', version='v1')
class CoordsApi(remote.Service):

    @endpoints.method(CoordinateMessage, # Request
                      ResponseMessage, # Response
                      path='coords',
                      http_method='POST',
                      name='guardar_coordenada')
    def guardar_coordenada(self, request):
        """
        Todas las instancias de las clases heredadas por Message,
        son serializadas a json automaticamente

        """

        # Saving in datastore
        coord = Coordinate(user=request.id_usuario,
                           geo_pos=ndb.GeoPt(request.latitud, request.longitud),
                           date_time=request.fecha_hora)
        coord.put()

        return ResponseMessage(value="Ok")


    @endpoints.method(QueryCoordMessage,
                      CoordinatesMessage,
                      path='coords',
                      http_method='GET',
                      name='leer_coordenadas')
    def leer_coordenadas(self, request):
         query = Coordinate.query(Coordinate.user == request.id_usuario)

         try:
             items = [ self._coordmodel_to_message(c) for c in query ]
             return CoordinatesMessage(items=items)
         except Exception, e:
             raise endpoints.NotFoundException(str(e))


    def _coordmodel_to_message(self, coord):
        return CoordinateMessage(id_usuario=coord.user,
                                 latitud=coord.geo_pos.lat,
                                 longitud=coord.geo_pos.lon,
                                 fecha_hora=coord.date_time)





APPLICATION = endpoints.api_server([CoordsApi])
