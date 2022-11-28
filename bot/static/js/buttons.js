createRowBot('Bem-vindo ao help IT chatbot espero que consigamos te auxiliar no seu problema. Clique em qual ferramenta está sendo problema:' +
    '</br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="sendButton(this.value);" value="Outlook">Outlook</button></br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="sendButton(this.value);" value="Cisco Jabber">Cisco Jabber</button></br><button id="buttonSay" class="btn btn-outline-dark mt-2" onClick="sendButton(this.value);" value="Citrix">Citrix</button>');



function sendButton(value){
                submitButton(value);
            }

function submitButton(value) {

            var inputData = {
              'text': value
            };
            console.log(inputData);

            var $submit = $.ajax({
                type: 'POST',
                url: chatterbotUrl,
                data: JSON.stringify(inputData),
                contentType: 'application/json',
                headers: {'X-CSRFToken': csrftoken},
                mode: 'same-origin'
            });

            $submit.done(function(statement) {
                createRowBot(statement.text);
            });

            $submit.fail(function() {
              // : Handle errors
            });
          }
