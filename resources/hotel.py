from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from resources.filtros import normalize_path_params, consulta_com_cidade, consulta_sem_cidade
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, Resource
from sql_alchemy import banco as db


class Hoteis(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cidade', type=str, location='args')
        parser.add_argument('estrelas_min', type=float, location='args', default=0)
        parser.add_argument('estrelas_max', type=float, location='args', default=5)
        parser.add_argument('diaria_min', type=float, location='args', default=0)
        parser.add_argument('diaria_max', type=float, location='args', default=10000)
        parser.add_argument('limit', type=int, location='args', default=50)
        parser.add_argument('offset', type=int, location='args', default=0)
        
        dados = parser.parse_args()
        
        # Normalização dos parâmetros
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        connection = None
        cursor = None
        
        try:
            # Obter conexão do SQLAlchemy
            engine = db.engine
            connection = engine.raw_connection()
            cursor = connection.cursor()
            
            # Preparar tupla de parâmetros na ordem correta
            if not parametros.get('cidade'):
                # ORDEM: estrelas_min, estrelas_max, diaria_min, diaria_max, limit, offset
                tupla = tuple([parametros[chave] for chave in parametros])
                cursor.execute(consulta_sem_cidade, tupla)
            else:
                # ORDEM: estrelas_min, estrelas_max, diaria_min, diaria_max, cidade, limit, offset
                tupla = tuple([parametros[chave] for chave in parametros])
                cursor.execute(consulta_com_cidade, tupla)
            
            resultados = cursor.fetchall()
            
            hoteis = []
            for linha in resultados:
                # Acesse pelos índices numéricos - ajuste conforme a ordem das colunas na sua tabela
                hoteis.append({
                    'hotel_id': linha[0],  # Primeira coluna - id
                    'nome': linha[1],      # Segunda coluna - nome
                    'estrelas': linha[2],  # Terceira coluna - estrelas
                    'diaria': float(linha[3]),  # Quarta coluna - diaria
                    'cidade': linha[4],    # Quinta coluna - cidade
                    'site_id': linha[5]    # Sexta coluna - site_id
                })

            return {'hoteis': hoteis}

        except Exception as err:
            return {'erro': f'Erro no banco de dados: {err}'}, 500
        
        finally:
            # Fechar recursos de forma segura
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()


class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    atributos.add_argument('estrelas')
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')
    atributos.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked with a site.")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 #Bad Request

        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        if not SiteModel.find_by_id(dados['site_id']):
            return {'message': 'The hotel must be associated to a valid site id.'}, 400

        try:
            hotel.save_hotel()
        except:
            return {"message": "An error ocurred trying to create hotel."}, 500 #Internal Server Error
        return hotel.json(), 201

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel.save_hotel()
        return hotel.json(), 201

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404
