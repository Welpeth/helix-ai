$(document).ready(function() {
    if (localStorage.getItem('dark-mode') === 'enabled') {
        $('body').addClass('dark-mode');
        $('#toggle-dark-mode').prop('checked', true);
    }

    // Alterna o modo escuro
    $('#toggle-dark-mode').change(function() {
        $('body').toggleClass('dark-mode');
        if ($('body').hasClass('dark-mode')) {
            localStorage.setItem('dark-mode', 'enabled');
        } else {
            localStorage.setItem('dark-mode', 'disabled');
        }
    });

    // Envia a mensagem ao clicar no botão
    $('#send-button').click(function() {
        sendMessage();
    });

    // Envia a mensagem ao pressionar Enter
    $('#user-input').keypress(function(e) {
        if (e.which === 13) { 
            e.preventDefault(); 
            sendMessage();
        }
    });

    // Função para enviar a mensagem
    function sendMessage() {
        var message = $('#user-input').val().trim();
        if (message !== '') {
            // Adiciona a mensagem do usuário ao chat
            const userMessageDiv = createMessage(message, false, false); 
            $('#chat-messages').append(userMessageDiv);
            $('#user-input').val('');

            // Faz o scroll para o final do chat
            $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);

            // Envia a mensagem para o backend
            $.ajax({
                url: '/handle_message',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ message: message }),
                success: function(data) {
                    // Checa se a resposta é a mensagem inicial
                    const initialMessage = "Olá eu sou Helix, seu assistente virtual.";
                    const botMessageDiv = createMessage('', true, true); 
                    $('#chat-messages').append(botMessageDiv);
                    $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);

                    if (data.response === initialMessage) {
                        updateMessageContent(botMessageDiv, data.response);
                        $(botMessageDiv).find('.typing-indicator').remove(); // Remove o indicador de digitação
                    } else {
                        updateMessageContent(botMessageDiv, data.response);
                        typeMessage(botMessageDiv); // Usa animação de digitação para outras mensagens
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Erro ao enviar a mensagem:', error);
                }
            });
        }
    }

    function createMessage(content, isBot = true, typing = false) {
        const messageDiv = $('<div class="message"></div>');
        if (isBot) {
            messageDiv.addClass('bot');
            const img = $('<img>').attr({
                src: '/static/images/helix-pic.png',
                alt: 'Bot',
                width: '40',
                height: '40'
            });
            messageDiv.append(img);
        } else {
            messageDiv.addClass('user');
        }

        // Cria o conteúdo da mensagem
        const messageContentDiv = $('<div class="message-content"></div>').text(content);
        messageDiv.append(messageContentDiv);

        if (isBot && typing) {
            const typingIndicatorDiv = $('<div class="typing-indicator"></div>');
            typingIndicatorDiv.css('display', 'flex'); 
            for (let i = 0; i < 3; i++) {
                const dotDiv = $('<div class="dot"></div>');
                typingIndicatorDiv.append(dotDiv);
            }
            messageDiv.append(typingIndicatorDiv);
        }

        return messageDiv;
    }

    function updateMessageContent(messageDiv, content) {
        $(messageDiv).find('.message-content').text(content);
    }

    function typeMessage(messageDiv) {
        const messageContentDiv = $(messageDiv).find('.message-content');
        const typingIndicatorDiv = $(messageDiv).find('.typing-indicator');
        const text = $(messageContentDiv).text(); // Usa o texto já definido
        let i = 0;

        $(messageContentDiv).text(''); // Limpa o texto atual

        function type() {
            if (i < text.length) {
                $(messageContentDiv).text($(messageContentDiv).text() + text.charAt(i));
                i++;
                setTimeout(type, 50); // Velocidade de digitação
            } else {
                if ($(messageDiv).hasClass('bot')) {
                    $(typingIndicatorDiv).css('display', 'none'); 
                }
            }
        }

        type();
    }

    function escapeHtml(text) {
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;')
            .replace(/\n/g, '<br>'); 
    }
});
