import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# 1. Configuração da página
st.set_page_config(page_title="App Libras PRO", page_icon="Logo_Libras.png", layout="wide")

# 2. Função para converter a imagem em código para injetar no HTML
def carregar_logo(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "rb") as arquivo:
            conteudo = arquivo.read()
            b64 = base64.b64encode(conteudo).decode()
            return f'<img src="data:image/png;base64,{b64}" style="width: 40px; height: 40px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'
    return '<span>🤟</span>'

logo_html = carregar_logo("Logo_Libras.png")

# Removemos o padding padrão do Streamlit para ocupar a tela toda
st.markdown("""
    <style>
        .block-container { padding-top: 0rem; padding-bottom: 0rem; padding-left: 0rem; padding-right: 0rem; max-width: 100%; }
        header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# CÓDIGO DO APLICATIVO WEB (HTML + CSS Responsivo + JS)
codigo_html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        
        body { 
            background-color: #f3f4f6; 
            color: #1f2937; 
            height: 100vh; 
            display: flex;
            overflow: hidden;
            flex-direction: row; /* Padrão para Desktop */
        }

        /* BARRA LATERAL (MENU) - Desktop */
        .sidebar {
            width: 260px;
            background-color: #ffffff;
            border-right: 1px solid #e5e7eb;
            display: flex;
            flex-direction: column;
            padding: 20px 0;
            box-shadow: 2px 0 5px rgba(0,0,0,0.02);
            z-index: 10;
        }

        .logo-area {
            padding: 0 20px 30px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            color: #10b981;
            font-size: 20px;
            font-weight: 700;
        }

        .menu-item {
            padding: 15px 25px;
            display: flex;
            align-items: center;
            gap: 12px;
            color: #4b5563;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            border-left: 4px solid transparent;
        }

        .menu-item:hover { background-color: #f0fdf4; color: #10b981; }
        .menu-item.active { 
            background-color: #ecfdf5; 
            color: #10b981; 
            border-left: 4px solid #10b981; 
        }

        /* ÁREA PRINCIPAL */
        .main-content {
            flex: 1;
            background-color: #f9fafb;
            position: relative;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }

        .aba-conteudo {
            display: none;
            height: 100%;
            flex-direction: column;
            padding: 20px;
        }

        .aba-conteudo.active { display: flex; }

        .header-aba {
            padding-bottom: 15px;
            border-bottom: 1px solid #e5e7eb;
            margin-bottom: 15px;
        }
        .header-aba h2 { color: #111827; font-size: 20px;}
        .header-aba p { color: #6b7280; font-size: 14px; margin-top: 5px; }

        /* MÓDULO 1: CHAT UNIFICADO */
        .chat-container {
            flex: 1;
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            border: 1px solid #e5e7eb;
            margin-bottom: 10px;
        }

        .chat-history {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
            background-color: #f8fafc;
        }

        .mensagem {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 16px;
            font-size: 15px;
            line-height: 1.4;
            cursor: pointer;
            position: relative;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        .msg-p1 {
            background-color: #d1fae5;
            color: #065f46;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }

        .msg-p2 {
            background-color: #ffffff;
            color: #1f2937;
            align-self: flex-end;
            border: 1px solid #e5e7eb;
            border-bottom-right-radius: 4px;
        }

        .chat-inputs {
            display: flex;
            background: #ffffff;
            padding: 12px;
            gap: 10px;
            border-top: 1px solid #e5e7eb;
            flex-direction: row; /* Desktop lado a lado */
        }

        .input-group {
            flex: 1;
            display: flex;
            background: #f3f4f6;
            border-radius: 25px;
            padding: 4px 4px 4px 15px;
            border: 1px solid transparent;
        }
        
        .input-group:focus-within { border-color: #10b981; background: #ffffff; }

        .input-group input {
            flex: 1;
            border: none;
            background: transparent;
            outline: none;
            font-size: 14px;
        }

        .btn-enviar {
            background: #10b981;
            color: white;
            border: none;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* MÓDULO 2 & 3: DICIONÁRIO E FRASES RÁPIDAS */
        .painel-centralizado {
            background: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            border: 1px solid #e5e7eb;
            text-align: center;
        }

        .input-grande {
            width: 100%;
            max-width: 500px;
            padding: 12px 15px;
            font-size: 16px;
            border: 2px solid #d1fae5;
            border-radius: 30px;
            outline: none;
            margin-bottom: 15px;
        }

        .texto-traducao {
            font-size: 20px;
            font-weight: 600;
            color: #065f46;
            padding: 15px;
            background: #ecfdf5;
            border-radius: 12px;
            display: inline-block;
            cursor: pointer;
            border: 1px dashed #10b981;
        }

        .grid-frases {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 10px;
        }

        .card-frase {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            padding: 15px;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 500;
            color: #374151;
            font-size: 14px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        /* ========================================================= */
        /* MEDIA QUERIES (A MÁGICA PARA O CELULAR)                   */
        /* ========================================================= */
        @media (max-width: 768px) {
            body {
                flex-direction: column; /* Muda a direção para coluna em telas pequenas */
            }

            .main-content {
                height: calc(100vh - 65px); /* Dá espaço para o menu inferior */
                padding-bottom: 0;
            }

            /* Transforma o menu lateral em menu inferior flutuante */
            .sidebar {
                width: 100%;
                height: 65px;
                flex-direction: row;
                justify-content: space-around;
                align-items: center;
                padding: 0;
                border-right: none;
                border-top: 1px solid #e5e7eb;
                position: fixed;
                bottom: 0;
                left: 0;
                z-index: 100;
                box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
            }

            .logo-area {
                display: none; /* Esconde a logo para liberar espaço na barra inferior */
            }

            .menu-item {
                flex: 1;
                flex-direction: column; /* Ícone em cima, texto embaixo */
                justify-content: center;
                padding: 5px;
                font-size: 12px;
                gap: 4px;
                border-left: none;
                border-top: 3px solid transparent;
            }

            .menu-item.active {
                border-left: none;
                border-top: 3px solid #10b981; /* O destaque ativo passa para cima */
                background-color: transparent;
            }

            .aba-conteudo {
                padding: 10px; /* Reduz margens na tela pequena */
            }

            /* Empilha as caixas de digitação para não ficarem espremidas */
            .chat-inputs {
                flex-direction: column; 
            }
            
            .mensagem {
                max-width: 90%;
            }
        }

    </style>
</head>
<body>

    <!-- BARRA LATERAL / INFERIOR (Depende do aparelho) -->
    <div class="sidebar">
        <div class="logo-area">
            [[MARCADOR_LOGO]] LIBRAS Pro
        </div>
        
        <div class="menu-item active" onclick="mudarAba('aba-chat', this)">
            <span style="font-size: 20px;">💬</span>
            <span>Conversa</span>
        </div>
        <div class="menu-item" onclick="mudarAba('aba-dicionario', this)">
            <span style="font-size: 20px;">📖</span>
            <span>Dicionário</span>
        </div>
        <div class="menu-item" onclick="mudarAba('aba-frases', this)">
            <span style="font-size: 20px;">⚡</span>
            <span>Rápido</span>
        </div>
    </div>

    <!-- ÁREA PRINCIPAL -->
    <div class="main-content">
        
        <!-- ABA 1: CHAT UNIFICADO -->
        <div id="aba-chat" class="aba-conteudo active">
            <div class="header-aba">
                <h2>Comunicação</h2>
                <p>Usem as caixas abaixo. Duplo clique para traduzir.</p>
            </div>
            
            <div class="chat-container">
                <div class="chat-history" id="chat-box">
                    <div class="mensagem msg-p1">Olá! Vamos começar?</div>
                </div>
                
                <div class="chat-inputs">
                    <div class="input-group">
                        <input type="text" id="input-p1" placeholder="Pessoa 1 digita..." onkeypress="teclaEnter(event, 'p1')">
                        <button class="btn-enviar" onclick="enviarChat('p1')">➤</button>
                    </div>
                    <div class="input-group">
                        <input type="text" id="input-p2" placeholder="Pessoa 2 digita..." onkeypress="teclaEnter(event, 'p2')">
                        <button class="btn-enviar" onclick="enviarChat('p2')" style="background-color: #374151;">➤</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- ABA 2: DICIONÁRIO -->
        <div id="aba-dicionario" class="aba-conteudo">
            <div class="header-aba">
                <h2>Dicionário</h2>
                <p>Pesquise palavras isoladas.</p>
            </div>
            
            <div class="painel-centralizado">
                <input type="text" id="input-dicionario" class="input-grande" placeholder="Ex: Obrigado..." oninput="atualizarDicionario()">
                <br>
                <div style="font-size:12px; color:#6b7280; margin-bottom:10px;">💡 Duplo clique abaixo para traduzir</div>
                <div id="resultado-dicionario" class="texto-traducao">...</div>
            </div>
        </div>

        <!-- ABA 3: FRASES RÁPIDAS -->
        <div id="aba-frases" class="aba-conteudo">
            <div class="header-aba">
                <h2>Acesso Rápido</h2>
                <p>Duplo clique para comunicar rápido.</p>
            </div>
            
            <div class="grid-frases">
                <div class="card-frase">Bom dia! Tudo bem?</div>
                <div class="card-frase">Qual é o seu nome?</div>
                <div class="card-frase">Pode me ajudar?</div>
                <div class="card-frase">Eu não entendi.</div>
                <div class="card-frase">Muito obrigado</div>
                <div class="card-frase">Com licença</div>
                <div class="card-frase">Onde fica o banheiro?</div>
                <div class="card-frase">Tenho uma dúvida</div>
            </div>
        </div>

    </div>

    <!-- WIDGET VLIBRAS -->
    <div vw class="enabled">
        <div vw-access-button class="active"></div>
        <div vw-plugin-wrapper>
            <div class="vw-plugin-top-wrapper"></div>
        </div>
    </div>
    
    <script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
    <script>
        new window.VLibras.Widget('https://vlibras.gov.br/app');

        function mudarAba(idAba, elementoClicado) {
            document.querySelectorAll('.aba-conteudo').forEach(aba => {
                aba.classList.remove('active');
            });
            document.querySelectorAll('.menu-item').forEach(item => {
                item.classList.remove('active');
            });
            
            document.getElementById(idAba).classList.add('active');
            elementoClicado.classList.add('active');
        }

        function limparTexto(texto) {
            return texto.replace(/[.,!?]/g, '').trim();
        }

        function enviarChat(pessoa) {
            const input = document.getElementById('input-' + pessoa);
            const texto = input.value;
            
            if(texto.trim() === '') return;

            const chatBox = document.getElementById('chat-box');
            const novaMsg = document.createElement('div');
            
            novaMsg.className = 'mensagem ' + (pessoa === 'p1' ? 'msg-p1' : 'msg-p2');
            novaMsg.textContent = limparTexto(texto);

            chatBox.appendChild(novaMsg);
            input.value = '';
            
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function teclaEnter(event, pessoa) {
            if (event.key === 'Enter') enviarChat(pessoa);
        }

        function atualizarDicionario() {
            const texto = document.getElementById('input-dicionario').value;
            const resultado = document.getElementById('resultado-dicionario');
            resultado.textContent = texto.trim() === '' ? '...' : limparTexto(texto);
        }
    </script>
</body>
</html>
"""

# Injeta a tag de imagem pronta no lugar do marcador dentro do HTML
codigo_html = codigo_html.replace('[[MARCADOR_LOGO]]', logo_html)

# Renderiza com uma altura alta para preencher tudo na tela de celulares
components.html(codigo_html, height=1000, scrolling=False)
