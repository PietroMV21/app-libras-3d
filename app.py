import streamlit as st
import streamlit.components.v1 as components

# 1. Configuração inicial da página
st.set_page_config(
    page_title="Tradutor de Libras 3D",
    page_icon="🤟",
    layout="centered"
)

# 2. Cabeçalho do App
st.title("Tradutor de Texto para Libras 🤟")
st.write("Bem-vindo! Digite a mensagem que você deseja transmitir, e nosso Avatar 3D fará a tradução para a Língua Brasileira de Sinais.")

# 3. Caixa de entrada para o usuário digitar a mensagem
texto_usuario = st.text_area(
    "Digite sua mensagem aqui:", 
    "Olá! Como posso ajudar você hoje?"
)

st.markdown("---")
st.subheader("Tradução em Libras")

# 4. Criação do bloco HTML que une o texto ao tradutor VLibras
codigo_html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #ffffff;
            padding: 10px;
        }}
        .caixa-texto {{
            font-size: 20px;
            color: #2c3e50;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #3498db;
            margin-bottom: 20px;
        }}
        .instrucao {{
            color: #e74c3c;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <p class="instrucao">👉 Instruções: Clique no ícone azul com as mãos (à direita) e depois clique duas vezes sobre o texto abaixo.</p>
    
    <div class="caixa-texto">
        {texto_usuario}
    </div>

    <!-- Código oficial de integração do VLibras -->
    <div vw class="enabled">
        <div vw-access-button class="active"></div>
        <div vw-plugin-wrapper>
            <div class="vw-plugin-top-wrapper"></div>
        </div>
    </div>
    <script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
    <script>
        new window.VLibras.Widget('https://vlibras.gov.br/app');
    </script>
</body>
</html>
"""

# 5. Renderizando o HTML dentro do Streamlit
components.html(codigo_html, height=500, scrolling=True)

# 6. Rodapé
st.caption("Protótipo desenvolvido para acessibilidade utilizando Streamlit e a suíte VLibras.")
