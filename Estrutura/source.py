import requests, difflib, os


# Configurações do SonarQube
SONARQUBE_URL = os.getenv('SONAR_URL')
TOKEN = os.getenv('sonar_token')
PROJECT_KEY = os.getenv('SONAR_PROJECT_KEY')

def resolve_error(component_path, line, start_offset, end_offset, message):
    # Função para resolver um erro específico no código baseado na análise do SonarQube
    
    # Verifica se a linha e os offsets foram fornecidos
    if line and start_offset is not None and end_offset is not None:
        similaridade_minima = 0.49  # Define o limite mínimo de similaridade (0 a 1) para considerar duas palavras como similares
        
        # Abrir o arquivo de código e ler todas as linhas
        with open(component_path, 'r') as file:
            lines = file.readlines()

        # Seleciona a linha específica onde o erro foi identificado e a divide em palavras
        error_line = lines[line-1].split()

        # Divide a mensagem de erro do SonarQube em palavras
        erro_sq = message.split()
    
    # Substituição de palavras similares entre a linha de código e a mensagem de erro
    for palavra1 in error_line:
        for palavra2 in erro_sq:
            # Utiliza a biblioteca difflib para calcular a similaridade entre as palavras
            similaridade = difflib.SequenceMatcher(None, palavra1, palavra2).ratio()
            
            if similaridade > similaridade_minima:
                # Se a similaridade for maior que o mínimo definido, substitui a palavra no código
                print(f'Palavras similares encontradas: "{palavra1}" e "{palavra2}" com similaridade de {similaridade:.2f}')
                lines[line-1] = lines[line-1].replace(palavra1, palavra2)
    
    # Escreve as alterações feitas no código de volta no arquivo
    with open(component_path, "w") as arquivo:
        arquivo.writelines(lines)

def code_request():
    # Função para fazer uma requisição à API do SonarQube e processar os problemas encontrados
    
    try:
        # Realiza uma requisição GET à API do SonarQube para buscar problemas no código do projeto especificado
        response = requests.get(f'{SONARQUBE_URL}/api/issues/search', auth=(TOKEN, ''),
                                params={
                                    'projectKeys': PROJECT_KEY,
                                    'statuses': 'OPEN',  # Filtra para issues abertas
                                })
    except Exception as e:
        print(f'Erro na requisição {e}')
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Processa a resposta da API como um JSON
        arq = response.json()
        # Filtra as issues para garantir que apenas as do projeto atual sejam processadas
        filtred_issues = [issue for issue in arq.get('issues', []) if issue['project'] == PROJECT_KEY] 
        
        if filtred_issues:
            # Itera sobre as issues filtradas
            for issue in filtred_issues:
                message = issue['message']  # Mensagem de erro do SonarQube
                severity = issue['severity']  # Severidade do problema
                line = issue.get('line')  # Linha onde o problema foi identificado
                component = issue['component']  # Componente (arquivo) onde o problema está localizado
                text_range = issue.get('textRange', {})  # Faixa de texto específica do problema
                print(f"Problema: {message} - Severidade: {severity} - linha: {int(line-1)}")

            # Obtém os offsets de início e fim do erro, se disponíveis
            start_offset = text_range.get('startOffset', None)
            end_offset = text_range.get('endOffset', None)

            # Converte o nome do componente (arquivo) em um caminho de arquivo local
            component_path = component.replace(f'{PROJECT_KEY}:', './')
            
            # Chama a função para tentar resolver o erro
            resolve_error(component_path, line, start_offset, end_offset, message)
        else:
            print(f'O projeto <{PROJECT_KEY}> não possui issues abertas!')
    else:
        # Caso a requisição não seja bem-sucedida, exibe uma mensagem de erro
        print(f"Erro ao acessar o código-fonte: {response.status_code} - {response.text}")

# Chama a função para iniciar o processo de requisição e resolução de erros
code_request()
