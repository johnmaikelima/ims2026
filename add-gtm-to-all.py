import os
import re

# Código GTM para adicionar
GTM_HEAD = """    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-PS83V9WS');</script>
    <!-- End Google Tag Manager -->
    
"""

GTM_BODY = """    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PS83V9WS"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
    
"""

def add_gtm_to_file(filepath):
    """Adiciona GTM a um arquivo HTML se ainda não tiver"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se já tem GTM
        if 'GTM-PS83V9WS' in content:
            print(f"✓ Já tem GTM: {filepath}")
            return False
        
        # Adiciona GTM no head (após <head>)
        if '<head>' in content and '<!-- Google Tag Manager -->' not in content:
            content = content.replace('<head>\n', '<head>\n' + GTM_HEAD, 1)
        
        # Adiciona GTM no body (após <body> ou <body data-page-level="...">)
        body_pattern = r'(<body[^>]*>\n)'
        if re.search(body_pattern, content) and '<!-- Google Tag Manager (noscript) -->' not in content:
            content = re.sub(body_pattern, r'\1' + GTM_BODY, content, count=1)
        
        # Salva o arquivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ GTM adicionado: {filepath}")
        return True
    
    except Exception as e:
        print(f"✗ Erro em {filepath}: {e}")
        return False

def process_directory(directory):
    """Processa todos os arquivos HTML em um diretório"""
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if add_gtm_to_file(filepath):
                    count += 1
    return count

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 60)
    print("Adicionando Google Tag Manager em todas as páginas HTML")
    print("=" * 60)
    
    # Processa páginas de serviços
    servicos_dir = os.path.join(base_dir, 'servicos')
    if os.path.exists(servicos_dir):
        print(f"\n📁 Processando: servicos/")
        count = process_directory(servicos_dir)
        print(f"   {count} arquivos atualizados")
    
    # Processa páginas de informações
    info_dir = os.path.join(base_dir, 'informacoes')
    if os.path.exists(info_dir):
        print(f"\n📁 Processando: informacoes/")
        count = process_directory(info_dir)
        print(f"   {count} arquivos atualizados")
    
    print("\n" + "=" * 60)
    print("✅ Concluído! Todas as páginas agora têm o Google Tag Manager")
    print("=" * 60)
