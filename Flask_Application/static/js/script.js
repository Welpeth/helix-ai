$(document).ready(function() {
    // Verifica se o modo escuro está salvo no localStorage
    if (localStorage.getItem('dark-mode') === 'enabled') {
        $('body').addClass('dark-mode');
        $('#toggle-dark-mode').prop('checked', true);
    }

    $('#toggle-dark-mode').change(function() {
        $('body').toggleClass('dark-mode');
        // Salva a preferência do usuário no localStorage
        if ($('body').hasClass('dark-mode')) {
            localStorage.setItem('dark-mode', 'enabled');
        } else {
            localStorage.setItem('dark-mode', 'disabled');
        }
    });

    $('#send-button').click(function () {
        sendMessage();
    });

    $('#user-input').keypress(function(e) {
        if (e.which == 13) {
            sendMessage();
        }
    });

    function sendMessage() {
        var message = $('#user-input').val().trim();
        if (message != '') {
            // Adiciona a mensagem do usuário ao chat
            $('#chat-messages').append('<div class="message user"><div class="message-content">' + escapeHtml(message) + '</div></div>');
            $('#user-input').val('');

            // Envia a mensagem para o backend
            $.ajax({
                url: '/handle_message',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({message: message}),
                success: function (data) {
                    // Adiciona uma mensagem de carregamento enquanto anima a resposta
                    const botMessage = $('<div class="message bot"><img src="/static/images/helix-pic.png" alt="Bot"><div class="message-content"></div></div>');
                    $('#chat-messages').append(botMessage);
                    $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);
                    
                    // Anima a resposta do bot
                    typeEffect(botMessage.find('.message-content')[0], data.response, 50);
                }
            });
        }
    }

    function escapeHtml(text) {
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;')
            .replace(/\n/g, '<br>'); // Adiciona essa linha para converter quebras de linha
    }
});

// Função para animar a escrita do texto
function typeEffect(element, text, speed) {
    let i = 0;
    element.innerHTML = ''; // Limpa o conteúdo anterior
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}
