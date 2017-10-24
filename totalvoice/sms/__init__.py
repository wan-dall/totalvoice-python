# coding=utf-8

from totalvoice.cliente import Cliente
from totalvoice.helper import utils
from totalvoice.helper.routes import Routes
from totalvoice.totalvoice import Totalvoice
import json, requests

class Sms(Totalvoice):
    cliente = None

    def __init__(self, cliente):
        self.cliente = cliente

    def enviar(self, numero_destino, mensagem, resposta_usuario=None, multi_sms=None):
        """
        :Descrição:

        Função para enviar mensagens de texto.

        :Utilização:

        enviar(self, numero_destino, mensagem, resposta_usuario, multi_sms)

        :Parâmetros:
        
        - numero_destino:
        Número do telefone que irá receber a mensagem, formato DDD + Número exemplo: 4832830151

        - mensagem:
        Mensagem de texto para ser enviada, limite: 160 caracteres não aceita acentos

        - resposta_usuario:
        Aguardar uma resposta do destinatário. true ou false. (Opcional)

        - multi_sms:
        Aceita SMS com mais de 160 char - ate 16.000. Envia multiplos sms para o mesmo numero (um a cada 160 char) e retorna array de ids. Default false. (Opcional)

        """
        host = self.buildHost(self.cliente.host, Routes.SMS)
        data = self.__buildSms(numero_destino, mensagem, resposta_usuario, multi_sms)
        response = requests.post(host, headers=utils.buildHeader(self.cliente.access_token), data=data)
        return response.content

    def getById(self, id):
        """
        :Descrição:

        Função para buscar informações de SMS e respostas.

        :Utilização:

        getById(id)

        :Parâmetros:

        - id:
        ID do sms.
        """
        host = self.buildHost(self.cliente.host, Routes.SMS, [id])
        return self.getRequest(host)

    def getRelatorio(self, data_inicio, data_fim):
        """
        :Descrição:
        
        Função para pegar o relatório de sms.

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
        host = self.buildHost(self.cliente.host, Routes.SMS, ["relatorio"])
        params = (('data_inicio', data_inicio),('data_fim', data_fim),)
        return self.getRequest(host, params)

    def __buildSms(self, numero_destino, mensagem, resposta_usuario, multi_sms):
        data = {}
        data.update({"numero_destino" : numero_destino})
        data.update({"mensagem" : mensagem})
        data.update({"resposta_usuario" : resposta_usuario})
        data.update({"multi_sms" : multi_sms})
        return json.dumps(data)