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

    
    chatterbot = ChatBot('Help-It')
    # trainer = ChatterBotCorpusTrainer(chatterbot)
    # trainer.train('chatterbot.corpus.portuguese')
    # trainer = ListTrainer(chatterbot)
    # trainer.train([
    #     'Oi',
    #     'Olá sou o Help-it, como posso te ajudar?',
    #     'O que você faz?',
    #     'Sou um chatbot, posso te ajudar com dúvidas sobre a área de tecnologia',
    #     'Qual a sua função?',
    #     'Sou um chatbot, posso te ajudar com dúvidas sobre a área de tecnologia',
    #     'Qual o seu nome?',
    #     'Meu nome é Help-it',
    # ])




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
        response_data['in_response_to'] = response_data['in_response_to'].lower().replace('-','')  # Remove "-" and change for lower
        response_data['in_response_to'] = unidecode(response_data['in_response_to']) # Remove accents
        # region Welcome
        if response_data['in_response_to'] == 'ola' or response_data['in_response_to'] == 'oi' or response_data[
             'in_response_to'] == 'olá' or response_data['in_response_to'] == 'começar':
             response_data[
                 'text'] = 'Bem-vindo ao help IT chatbot espero que consigamos te auxiliar no seu problema. Clique em qual ferramenta está sendo problema:' + \
                           '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="sendButton(this.value);" value="Outlook">Outlook</button>' + \
                           '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="sendButton(this.value);" value="Cisco Jabber">Cisco Jabber</button>' + \
                           '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="sendButton(this.value);" value="Citrix">Citrix</button>'

        elif response_data['in_response_to'] == 'desejo entender mais sobre as areas de ti':
             response_data['text'] = '????'
        # endregion

        # region outlook
        elif response_data['in_response_to'] == 'outlook':
             response_data['text'] = 'Em qual área você precisa de ajuda:</br>' + \
                                    'Outlook – Siga as seguintes instruções</br>' + \
                                    '1.	Cheque se está conectado com a internet</br>'+ \
                                    '2.	Reinicie o computador</br>'+ \
                                    '3.	Passando atendimento para analista de 2° nível</br>' + \
                                    '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="sendButton(this.value);" value="oi">Voltar ao início</button>'

        # endregion
        #region Cisco Jabber
        elif response_data['in_response_to'] == 'cisco jabber':
             response_data['text'] = 'Cisco Jabber - Siga as seguintes instruções:</br>' + \
                                    '1.	Cheque se está conectado com a internet</br>'+ \
                                    '2.	Reinicie o computador</br>'+ \
                                    '3.	Passando atendimento para analista de 2° nível</br>' + \
                                    '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="sendButton(this.value);" value="oi">Voltar ao início</button>'
        # endregion
        #region Citrix
        elif response_data['in_response_to'] == 'citrix':
                response_data['text'] = 'Citrix - Siga as seguintes instruções:</br>' + \
                    '1.	Cheque se está conectado com a internet</br>'+\
                    '2.	Reinicie o computador</br>'+\
                    '3.	Passando atendimento para analista de 2° nível</br>'+\
                    '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="sendButton(this.value);" value="oi">Voltar ao início</button>'

        # endregion
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
        'title': 'Help IT - Home Page',
    }
    return render(request, "html/index.html", context)
