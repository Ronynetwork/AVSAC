import requests, os
SONARQUBE_URL = "http://localhost:9000"
TOKEN = 'squ_18f50c8103d21125ca3ef38358475280bccdedfd'
PROJECT_KEY = 'AVSAC'

components_msg = {}
components = []

try:
    # Requisição para obter os problemas do projeto
    response = requests.get(
        f"{SONARQUBE_URL}/api/issues/search?componentKeys={PROJECT_KEY}",
        auth=(TOKEN, '')
    )
    arq = response.json()
    
    # Separando o retorno da requisição
    for issue in arq.get('issues', []):
        issue_id = issue['key']
        message = issue['message']
        severity = issue['severity']
        line = int(issue['textRange']['startLine'])
        component = issue['component']
        if component not in components_msg:
            components_msg[component] = [{
            "messages": message,
            "severity": severity,
            "line": line,
            }]
        else:
            components_msg[component].append({
                "messages": message,
                "severity": severity,
                "line": int(line), 
            })

except Exception as e:
    print(f"Erro ao obter problemas do projeto: {e}")

# Dados de exemplo (substitua pelos dados reais do seu script)
errors = []
for path in components_msg.keys():
    try:
        response_code = requests.get(
            f"{SONARQUBE_URL}/api/sources/raw?key={path}",
            auth=(TOKEN, '')
        )
        code = response_code.text.splitlines()
        path_split = path.replace(f'{PROJECT_KEY}:', '')
        
        # Adicionando os erros à lista
        details = components_msg[path]
        for det in details:
            error_entry = {
                "file": path_split,
                "message": det['messages'],
                "severity": det['severity'],
                "line": det['line'],
                "code": code[det['line'] - 1] if det['line'] - 1 < len(code) else ""
            }
            errors.append(error_entry)
    except Exception as e:
        print(f"Erro ao obter código-fonte do componente {path}: {e}")

# Criação do conteúdo HTML
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SonarQube Notification</title>
    <link rel="stylesheet" href="style.css"> <!-- Referência ao arquivo CSS externo -->
</head>
<body>
    <div class="notification">
        <p><strong>SonarQube Issues:</strong></p>
        <button id="toggleAll" class="toggle-all">Show All</button>
'''

# Itera sobre a lista de erros para adicionar ao HTML
for index, error in enumerate(errors):
    html_content += f'''
        <div class="error" id="error{index + 1}">
            <h3 class="error-title">{error["file"]} <span class="toggle-icon"></span></h3>
            <div class="error-details">
                <p>Message: {error["message"]} at line {error["line"]}</p>
                <p>Severity: {error["severity"]}</p>
                <p>Line in Code: {error["code"]}</p>
            </div>
        </div>
    '''

# Fechando as tags HTML
html_content += '''
    </div>
    <script src="script_java.js"></script>
</body>
</html>
'''

# Salvando o HTML em um arquivo
path_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(path_dir, 'sonarqube-notification.html')

with open(file_path, 'w') as file:
    file.write(html_content)

print("HTML gerado com sucesso!")
