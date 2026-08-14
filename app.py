import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# 1. Configuração da página
st.set_page_config(page_title="App Libras PRO", page_icon="Logo_Libras.png", layout="wide", initial_sidebar_state="collapsed")

# 2. Função para converter a logo
def carregar_logo(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "rb") as arquivo:
            conteudo = arquivo.read()
            b64 = base64.b64encode(conteudo).decode()
            return f'<img src="data:image/png;base64,{b64}" style="width: 40px; height: 40px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'
    return '<span>🤟</span>'

logo_html = carregar_logo("Logo_Libras.png")

# INJEÇÃO CSS NO STREAMLIT
st.markdown("""
    <style>
        header { visibility: hidden !important; display: none !important; }
        footer { visibility: hidden !important; display: none !important; }
        #MainMenu { visibility: hidden !important; display: none !important; }
        .viewerBadge_container__1QSob { display: none !important; }
        
        html, body, [data-testid="stAppViewContainer"], [data-testid="stAppScroll"] {
            overflow: hidden !important; 
            height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        iframe {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            height: 100dvh !important; 
            z-index: 999999 !important;
            border: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# CÓDIGO DO APLICATIVO WEB
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
            position: fixed; 
            top: 0; bottom: 0; left: 0; right: 0;
            display: flex;
            overflow: hidden; 
            overscroll-behavior-y: none; 
            flex-direction: row; 
        }

        .svg-icon {
            width: 24px;
            height: 24px;
            stroke: currentColor;
            stroke-width: 2;
            stroke-linecap: round;
            stroke-linejoin: round;
            fill: none;
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
            z-index: 100;
            position: relative;
        }

        .logo-area {
            padding: 0 20px 30px 20px;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            color: #10b981;
            font-size: 20px;
            font-weight: 700;
            gap: 12px;
        }
        
        /* Contêiner para empurrar o botão de info para o final da sidebar no PC */
        .menu-items-container {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        /* BOTÃO DE INFORMAÇÃO - PC (No canto inferior esquerdo) */
        .btn-info-desktop {
            background: none;
            border: none;
            color: #9ca3af;
            cursor: pointer;
            padding: 15px 25px;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 12px;
            font-weight: 500;
            transition: all 0.2s;
            margin-top: auto; /* Empurra para o fundo */
            border-top: 1px solid #f3f4f6;
        }
        .btn-info-desktop:hover { color: #10b981; background: #f0fdf4; }

        .menu-item {
            padding: 15px 25px;
            display: flex;
            align-items: center;
            gap: 12px;
            color: #6b7280;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            border-left: 4px solid transparent;
        }
        .menu-item:hover { background-color: #f0fdf4; color: #10b981; }
        .menu-item.active { background-color: #ecfdf5; color: #10b981; border-left: 4px solid #10b981; }

        /* ÁREA PRINCIPAL */
        .main-content {
            flex: 1;
            background-color: #f9fafb;
            display: flex;
            flex-direction: column;
            height: 100%;
            overflow: hidden; 
        }

        .aba-conteudo { display: none; height: 100%; flex-direction: column; padding: 20px; overflow-y: auto; }
        .aba-conteudo.active { display: flex; }

        .header-aba { padding-bottom: 15px; border-bottom: 1px solid #e5e7eb; margin-bottom: 15px; flex-shrink: 0; }
        .header-aba h2 { color: #111827; font-size: 20px;}
        .header-aba p { color: #6b7280; font-size: 14px; margin-top: 5px; }

        /* MÓDULOS (Chat, Dicionário, Frases) */
        .chat-container { flex: 1; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); display: flex; flex-direction: column; overflow: hidden; border: 1px solid #e5e7eb; margin-bottom: 10px; }
        .chat-history { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; background-color: #f8fafc; -webkit-overflow-scrolling: touch; }
        .mensagem { max-width: 80%; padding: 12px 16px; border-radius: 16px; font-size: 15px; line-height: 1.4; cursor: pointer; position: relative; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
        .msg-p1 { background-color: #d1fae5; color: #065f46; align-self: flex-start; border-bottom-left-radius: 4px; }
        .msg-p2 { background-color: #ffffff; color: #1f2937; align-self: flex-end; border: 1px solid #e5e7eb; border-bottom-right-radius: 4px; }
        .chat-inputs { display: flex; background: #ffffff; padding: 12px; gap: 10px; border-top: 1px solid #e5e7eb; flex-direction: row; flex-shrink: 0; }
        .input-group { flex: 1; display: flex; background: #f3f4f6; border-radius: 25px; padding: 4px 4px 4px 15px; border: 1px solid transparent; }
        .input-group:focus-within { border-color: #10b981; background: #ffffff; }
        .input-group input { flex: 1; border: none; background: transparent; outline: none; font-size: 14px; }
        .btn-enviar { background: #10b981; color: white; border: none; width: 36px; height: 36px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; }
        
        .painel-centralizado { background: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid #e5e7eb; text-align: center; }
        .input-grande { width: 100%; max-width: 500px; padding: 12px 15px; font-size: 16px; border: 2px solid #d1fae5; border-radius: 30px; outline: none; margin-bottom: 15px; }
        .texto-traducao { font-size: 20px; font-weight: 600; color: #065f46; padding: 15px; background: #ecfdf5; border-radius: 12px; display: inline-block; cursor: pointer; border: 1px dashed #10b981; }
        .grid-frases { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; padding-bottom: 20px; }
        .card-frase { background: #ffffff; border: 1px solid #e5e7eb; padding: 15px; border-radius: 12px; cursor: pointer; font-weight: 500; color: #374151; font-size: 14px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }

        /* MODAL DE INFORMAÇÕES (O Pop-up) */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.5);
            z-index: 999999;
            align-items: center;
            justify-content: center;
            padding: 20px;
            backdrop-filter: blur(3px);
        }
        .modal-box {
            background: white;
            border-radius: 16px;
            padding: 25px;
            max-width: 450px;
            width: 100%;
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
            border-top: 5px solid #10b981;
        }
        .modal-title { font-size: 18px; font-weight: bold; color: #1f2937; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;}
        .modal-text { font-size: 14px; color: #4b5563; line-height: 1.5; margin-bottom: 20px; }
        .modal-buttons { display: flex; flex-direction: column; gap: 10px; }
        .btn-modal-primary { background: #10b981; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; text-align: center;}
        
        .btn-modal-secondary { 
            background: transparent; 
            color: #6b7280; 
            border: 1px solid #d1d5db; 
            padding: 12px; 
            border-radius: 8px; 
            font-weight: bold; 
            cursor: pointer; 
            text-align: center;
            width: 100%;
        }
        .btn-modal-secondary:hover { background: #f3f4f6; color: #374151; }

        /* MODO CELULAR MÁGICO */
        @media (max-width: 768px) {
            body { flex-direction: column; }

            .sidebar {
                width: 100%; height: 75px; flex-direction: row; justify-content: space-around; align-items: center;
                padding: 0 10px; border-right: none; border-top: 1px solid #e5e7eb; position: absolute; bottom: 0; left: 0;
                z-index: 9999; background-color: #ffffff; box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
            }

            .main-content { position: absolute; top: 0; bottom: 75px; left: 0; right: 0; height: auto; }
            .logo-area { display: none; }
            .btn-info-desktop { display: none; } /* Esconde o botão inferior no celular */
            .menu-items-container { flex-direction: row; flex: 1; }

            /* Ícone de Info no Celular - Fica flutuando no topo direito */
            .btn-info-mobile {
                display: flex !important;
                position: absolute;
                top: 15px;
                right: 15px;
                background: white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                z-index: 999;
                border: 1px solid #e5e7eb;
                padding: 5px;
                border-radius: 50%;
                cursor: pointer;
            }

            .menu-item { flex: 1; flex-direction: column; justify-content: center; padding: 8px 5px; font-size: 11px; font-weight: 600; gap: 6px; border-left: none; border-top: 3px solid transparent; border-radius: 0; }
            .menu-item.active { border-left: none; border-top: 3px solid #10b981; background-color: transparent; color: #10b981; }

            .aba-conteudo { padding: 15px 10px; }
            .header-aba { padding-right: 40px; }
            .chat-container { margin-bottom: 0; border-radius: 0; border-left: none; border-right: none; }
            .chat-inputs { flex-direction: column; padding: 10px; }
            .mensagem { max-width: 90%; }
        }

        /* Oculta botão mobile no Desktop por padrão */
        .btn-info-mobile { display: none; }

    </style>
</head>
<body>

    <!-- BOTÃO INFO (VISÍVEL SÓ NO CELULAR) -->
    <button class="btn-info-mobile" onclick="abrirModal()" title="Sobre o Projeto">
        <svg class="svg-icon" viewBox="0 0 24 24" style="width: 20px; height: 20px; stroke: #10b981;">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
        </svg>
    </button>

    <!-- JANELA MODAL (POP-UP) -->
    <div class="modal-overlay" id="infoModal">
        <div class="modal-box">
            <div class="modal-title">
                <svg class="svg-icon" viewBox="0 0 24 24" style="stroke: #10b981; width: 22px;"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                Sobre o LIBRAS Pro
            </div>
            <div class="modal-text">
                Este aplicativo utiliza a tecnologia <strong>VLibras</strong> (desenvolvida pelo Governo Federal) para traduzir textos para a Língua Brasileira de Sinais através de um Avatar 3D.<br><br>
                <strong>⚠️ Atenção:</strong> O modelo do VLibras ainda está em constante treinamento. Ele pode cometer erros de interpretação gramatical ou soletrar (datilologia) palavras que já possuem sinais estabelecidos.
            </div>
            <div class="modal-buttons">
                <button class="btn-modal-primary" onclick="fecharModal()">Entendi</button>
                <!-- O LINK AGORA USA UMA FUNÇÃO JS AGRESSIVA PARA ABRIR O NAVEGADOR -->
                <button class="btn-modal-secondary" onclick="forcarLinkExterno()">Ler mais sobre o VLibras</button>
            </div>
        </div>
    </div>

    <!-- BARRA LATERAL / INFERIOR -->
    <div class="sidebar">
        <div class="logo-area">
            [[MARCADOR_LOGO]] LIBRAS Pro
        </div>
        
        <div class="menu-items-container">
            <div class="menu-item active" onclick="mudarAba('aba-chat', this)">
                <svg class="svg-icon" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                <span>Conversa</span>
            </div>
            <div class="menu-item" onclick="mudarAba('aba-dicionario', this)">
                <svg class="svg-icon" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                <span>Dicionário</span>
            </div>
            <div class="menu-item" onclick="mudarAba('aba-frases', this)">
                <svg class="svg-icon" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
                <span>Rápido</span>
            </div>
        </div>

        <!-- BOTÃO INFO (VISÍVEL SÓ NO DESKTOP - Canto inferior esquerdo) -->
        <button class="btn-info-desktop" onclick="abrirModal()" title="Sobre o Projeto">
            <svg class="svg-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
            <span>Sobre o Projeto</span>
        </button>
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
                        <button class="btn-enviar" onclick="enviarChat('p1')">
                            <svg style="width:16px; height:16px; fill:white;" viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
                        </button>
                    </div>
                    <div class="input-group">
                        <input type="text" id="input-p2" placeholder="Pessoa 2 digita..." onkeypress="teclaEnter(event, 'p2')">
                        <button class="btn-enviar" onclick="enviarChat('p2')" style="background-color: #374151;">
                            <svg style="width:16px; height:16px; fill:white;" viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
                        </button>
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

        function abrirModal() { document.getElementById('infoModal').style.display = 'flex'; }
        function fecharModal() { document.getElementById('infoModal').style.display = 'none'; }

        // A MÁGICA PARA FORÇAR A SAÍDA DO WEBVIEW E DO IFRAME
        function forcarLinkExterno() {
            var url = 'https://www.gov.br/governodigital/pt-br/acessibilidade-e-usuario/vlibras';
            
            // Tenta criar um link invisível com a flag de sistema do WebView do Android
            var a = document.createElement('a');
            a.href = url;
            a.target = '_system'; 
            a.rel = 'noopener noreferrer';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            // Fallback: se o clique manual falhar, usa o redirecionamento pai
            setTimeout(function() {
                window.parent.location.href = url;
            }, 100);
        }

        function mudarAba(idAba, elementoClicado) {
            document.querySelectorAll('.aba-conteudo').forEach(aba => { aba.classList.remove('active'); });
            document.querySelectorAll('.menu-item').forEach(item => { item.classList.remove('active'); });
            document.getElementById(idAba).classList.add('active');
            elementoClicado.classList.add('active');
        }

        function limparTexto(texto) { return texto.replace(/[.,!?]/g, '').trim(); }

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

        function teclaEnter(event, pessoa) { if (event.key === 'Enter') enviarChat(pessoa); }
        function atualizarDicionario() {
            const texto = document.getElementById('input-dicionario').value;
            const resultado = document.getElementById('resultado-dicionario');
            resultado.textContent = texto.trim() === '' ? '...' : limparTexto(texto);
        }
    </script>
</body>
</html>
"""

codigo_html = codigo_html.replace('[[MARCADOR_LOGO]]', logo_html)

components.html(codigo_html, height=800, scrolling=False)
