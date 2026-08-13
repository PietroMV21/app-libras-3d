import streamlit as st
import streamlit.components.v1 as components

# Configuração da página para ocupar mais espaço na tela
st.set_page_config(
    page_title="Chat Acessível em Libras",
    page_icon="💬",
    layout="wide"
)

# Título fora do aplicativo web
st.markdown("<h2 style='text-align: center; color: #16a34a;'>Plataforma de Comunicação Acessível</h2>", unsafe_allow_html=True)
st.write("---")

# O CÓDIGO MÁGICO: Aqui criamos um mini-site dentro do Streamlit para evitar que a página recarregue.
# Aplicamos um design moderno, limpo, usando as cores Branco e Verde.
codigo_html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <style>
        /* Paleta de Cores Moderna: Branco e Verde */
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background-color: #f4fdf8; /* Verde bem clarinho para o fundo */
            margin: 0; 
            padding: 10px; 
            color: #1f2937; 
        }
        
        .instrucoes {
            text-align: center;
            background-color: #dcfce7;
            color: #15803d;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 15px;
            border: 1px solid #bbf7d0;
        }

        .container-chat { 
            display: flex; 
            gap: 20px; 
            justify-content: center; 
            height: 65vh; 
            min-height: 500px; 
        }
        
        /* Estilo das Colunas de Chat */
        .coluna-chat { 
            background: #ffffff; 
            border-radius: 12px; 
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); 
            flex: 1; 
            display: flex; 
            flex-direction: column; 
            max-width: 500px; 
            border: 1px solid #e5e7eb; 
            overflow: hidden; 
        }
        
        .cabecalho-chat { 
            background: #16a34a; /* Verde Vibrante */
            color: white; 
            padding: 15px; 
            text-align: center; 
            font-weight: bold; 
            font-size: 1.2rem; 
        }
        
        .historico-chat { 
            flex: 1; 
            padding: 20px; 
            overflow-y: auto; 
            display: flex; 
            flex-direction: column; 
            gap: 12px; 
            background: #fafafa; 
        }
        
        /* Estilo dos Balões de Mensagem */
        .balao-mensagem { 
            background: #dcfce7; /* Fundo verde claro do balão */
            padding: 12px 18px; 
            border-radius: 15px; 
            color: #065f46; 
            border-left: 5px solid #22c55e; 
            cursor: pointer; 
            transition: all 0.2s; 
            font-size: 1rem; 
            width: fit-content; 
            max-width: 85%; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .balao-mensagem:hover { 
            background: #bbf7d0; 
            transform: scale(1.02);
        }
        
        /* Área de Digitação */
        .area-input { 
            display: flex; 
            padding: 15px; 
            background: white; 
            border-top: 1px solid #f3f4f6; 
            gap: 10px; 
        }
        
        .caixa-texto { 
            flex: 1; 
            padding: 12px; 
            border: 1px solid #d1d5db; 
            border-radius: 8px; 
            font-size: 1rem; 
            outline: none; 
            transition: border-color 0.2s;
        }
        
        .caixa-texto:focus { 
            border-color: #16a34a; 
            box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.2);
        }
        
        .botao-enviar { 
            background: #16a34a; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 8px; 
            font-weight: bold; 
            cursor: pointer; 
            transition: background 0.2s; 
        }
        
        .botao-enviar:hover { 
            background: #15803d; 
        }
    </style>
</head>
<body>

    <div class="instrucoes">
        <strong>Como usar:</strong> Digite uma mensagem e clique em Enviar. Depois, <b>dê um duplo clique na mensagem enviada</b> para o Avatar 3D fazer a tradução!
    </div>

    <div class="container-chat">
        <!-- Coluna 1: Ouvinte -->
        <div class="coluna-chat">
            <div class="cabecalho-chat">Pessoa 1 (Ouvinte)</div>
            <div class="historico-chat" id="historico1">
                <div class="balao-mensagem">Olá! Como posso te ajudar hoje?</div>
            </div>
            <div class="area-input">
                <input type="text" id="input1" class="caixa-texto" placeholder="Digite aqui..." onkeypress="apertouEnter(event, 1)">
                <button class="botao-enviar" onclick="enviarMensagem(1)">Enviar</button>
            </div>
        </div>

        <!-- Coluna 2: Surdo/Libras -->
        <div class="coluna-chat">
            <div class="cabecalho-chat">Pessoa 2 (Libras)</div>
            <div class="historico-chat" id="historico2">
                <div class="balao-mensagem">Tudo bem! Pode me explicar o projeto?</div>
            </div>
            <div class="area-input">
                <input type="text" id="input2" class="caixa-texto" placeholder="Digite aqui..." onkeypress="apertouEnter(event, 2)">
                <button class="botao-enviar" onclick="enviarMensagem(2)">Enviar</button>
            </div>
        </div>
    </div>

    <!-- Script Oficial do VLibras -->
    <div vw class="enabled">
        <div vw-access-button class="active"></div>
        <div vw-plugin-wrapper>
            <div class="vw-plugin-top-wrapper"></div>
        </div>
    </div>
    <script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
    
    <!-- Lógica de funcionamento do Chat -->
    <script>
        // Inicia o Avatar
        new window.VLibras.Widget('https://vlibras.gov.br/app');

        // Função para adicionar a mensagem na tela sem recarregar
        function enviarMensagem(usuario) {
            const input = document.getElementById('input' + usuario);
            const texto = input.value.trim();
            
            if (texto === '') return; // Não envia mensagens vazias

            const historico = document.getElementById('historico' + usuario);
            
            // Cria o balão de mensagem novo
            const balao = document.createElement('div');
            balao.className = 'balao-mensagem';
            balao.textContent = texto;
            
            // Adiciona no histórico e limpa a caixa de texto
            historico.appendChild(balao);
            input.value = '';
            
            // Rola a tela para baixo automaticamente para ver a última mensagem
            historico.scrollTop = historico.scrollHeight;
        }

        // Função para permitir enviar apertando a tecla ENTER do teclado
        function apertouEnter(event, usuario) {
            if (event.key === 'Enter') {
                enviarMensagem(usuario);
            }
        }
    </script>
</body>
</html>
"""

# Renderiza o mini-site dentro do Streamlit com altura suficiente para caber tudo
components.html(codigo_html, height=800, scrolling=False)
