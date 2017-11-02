# coding=utf-8

from totalvoice.cliente import Cliente
from totalvoice.cliente.api.helper import utils
from totalvoice.cliente.api.helper.routes import Routes
from totalvoice.cliente.api.totalvoice import Totalvoice
import json, requests

class Audio(Totalvoice):
    cliente = None

    def __init__(self, cliente):
        self.cliente = cliente

    def enviar(self, numero_destino, url_audio, resposta_usuario=None, bina=None):
        """
        :Descrição:

        Essa é uma função para enviar um áudio para um número destino.

        :Utilização:

        enviar(numero_destino, url_audio, resposta_usuario, bina)

        :Parâmetros:
        
        - numero_destino:
        Número do telefone destino.

        - url_audio:
        URL do áudio a ser enviado.

        - resposta_usuario:
        Booleano que informa se o usuário pode responder o áudio.

        - bina:
        Número de bina para a chamada de áudio.
        """
        host = self.buildHost(self.cliente.host, Routes.AUDIO)
        data = self.__buildAudio(numero_destino, url_audio, resposta_usuario, bina)
        response = requests.post(host, headers=utils.buildHeader(self.cliente.access_token), data=data)
        return response.content

    def getById(self, id):
        """
        :Descrição:

        Função para buscar as informações de um audio.

        :Utilização:

        getById(id)

        :Parâmetros:

        - id:
        ID do audio.
        """
        host = self.cliente.host + Routes.AUDIO + "/" + id
        return self.getRequest(host)
    
    def getRelatorio(self, data_inicio, data_fim):
        """
        :Descrição:
        
        Função para pegar o relatório de áudios.

        :Utilização:

        getRelatorio(data_inicio, data_fim)

        :Parâmetros:

        - data_inicio:
        Data início do relatório (2016-03-30T17:15:59-03:00)
        format UTC

        - data_fim:
        Data final do relatório (2016-03-30T17:15:59-03:00)
        format UTC    

        """
        host = self.buildHost(self.cliente.host, Routes.AUDIO, ["relatorio"])
        params = (('data_inicio', data_inicio),('data_fim', data_fim),)
        return self.getRequest(host, params)

    def __buildAudio(self, numero_destino, url_audio, resposta_usuario=None, bina=None):
        data = {}
        data.update({"numero_destino" : numero_destino})
        data.update({"url_audio" : url_audio})
        data.update({"resposta_usuario" : resposta_usuario})
        data.update({"bina" : bina})
        return json.dumps(data)