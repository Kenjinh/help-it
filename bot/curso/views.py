import json
from datetime import datetime
from unidecode import unidecode
from chatterbot import ChatBot  # Import ChatBot
from . import models
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from chatterbot.trainers import ListTrainer  # Import ListTrainer from chatterbot
from django.views.decorators.csrf import csrf_exempt  # Import CSRF Token
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    
    chatterbot = ChatBot('Help-It', logic_adapters=['chatterbot.logic.BestMatch', 'chatterbot.logic.MathematicalEvaluation'],storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3'
    )
    trainer = ChatterBotCorpusTrainer(chatterbot)
    trainer.train('chatterbot.corpus.portuguese')
    trainer = ListTrainer(chatterbot)
    trainer.train([
        'Oi',
        'Olá sou o Help-it, como posso te ajudar?',
        'O que você faz?',
        'Sou um chatbot, posso te ajudar com dúvidas sobre a área de tecnologia',
    ])




    @csrf_exempt
    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.
        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))
        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        response = self.chatterbot.get_response(input_data)
        response_data = response.serialize()
        # response_data['in_response_to'] = response_data['in_response_to'].lower().replace('-','')  # Remove "-" and change for lower
        # response_data['in_response_to'] = unidecode(response_data['in_response_to']) # Remove accents
        # # region Welcome
        # if response_data['in_response_to'] == 'ola' or response_data['in_response_to'] == 'oi' or response_data[
        #     'in_response_to'] == 'olá' or response_data['in_response_to'] == 'começar':
        #     response_data[
        #         'text'] = 'Seja bem-vindo, sou o Help-it e estarei te auxiliando a escolher algum determinado curso ou auxiliando a aprender sobre algumas das áreas de TI!Escolha uma das seguintes opções:' + \
        #                   '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="sendButton(this.value);" value="Quero visualizar os cursos disponíveis">Quero visualizar os cursos disponíveis</button>'

        # elif response_data['in_response_to'] == 'desejo entender mais sobre as areas de ti':
        #     response_data['text'] = '????'
        # # endregion

        # # region Select Train
        # elif response_data['in_response_to'] == 'quero visualizar os cursos disponiveis':
        #     response_data['text'] = 'Em qual área você tem interesse em treinamentos:' + \
        #                             '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="var buttonValue = sendButton(this.value);" value="Desenvolvimento Front-end">Desenvolvimento Front-end</button>' + \
        #                             '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="var buttonValue = sendButton(this.value);" value="Desenvolvimento Back-end">Desenvolvimento Back-end</button>' + \
        #                             '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="var buttonValue = sendButton(this.value);" value="Mobile">Desenvolvimento Mobile</button>' + \
        #                             '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="var buttonValue = sendButton(this.value);" value="git e github">Versionamento de códigos com Git e GitHub</button>' + \
        #                             '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="var buttonValue = sendButton(this.value);" value="Redes de computadores">Redes de computadores</button>' + \
        #                             '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="var buttonValue = sendButton(this.value);" value="automação">Criação de automação de testes</button>' + \
        #                             '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="var buttonValue = sendButton(this.value);" value="Banco de dados">Banco de dados</button>' + \
        #                             '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="var buttonValue = sendButton(this.value);" value="ola">Voltar ao menu inicial</button>'
        # # endregion
        return JsonResponse(response_data, status=200)

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        print(request)
        print(self)
        return JsonResponse({
            'name': self.chatterbot.name
        })


def home(request):
    context = {
        'year': datetime.now().year,
        'title': 'Home Page',
    }
    return render(request, "html/index.html", context)
