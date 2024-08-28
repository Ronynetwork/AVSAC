import requests, os


# Configurações do SonarQube
SONARQUBE_URL = "http://localhost:9000"
TOKEN = "squ_7b34b7a3dc25566deb28a91cb04dee7a7c502f07"
PROJECT_KEY = 'AVSAC'

    # Componente do arquivo desejado
try:
    response = requests.get(
        f"{SONARQUBE_URL}/api/issues/search?componentKeys={PROJECT_KEY}",
        auth=(TOKEN, '')
    )

    # Formatando a resposta com o JSON e definindo as variaveis com a lista de dicionarios resultante do GET
    arq = response.json()
    components_msg = dict()
    components = list()
    for issue in arq.get('issues', []):
        message = issue['message']
        severity = issue['severity']
        line = issue['textRange']['startLine']
        component = issue['component']
        text_range = issue.get('textRange', {})
        error = issue.get('errors')
        if component not in components:
            components.append(component)
            components_msg[component] = [message, severity, line]
    try:
        for path in components:
            response_code = requests.get(
                f"{SONARQUBE_URL}/api/sources/raw?key={path}",
                auth=(TOKEN, '')
            )
            # Armazenando o codigo escaneado e dividindo em linhas
            code = response_code.text
            lines = code.splitlines()
            path_split = path.replace(f'{PROJECT_KEY}:','')
    # Formatando a variavel component para remover a key do projeto e definir apenas o PATH
    except Exception as e:
        # Caso a resposta não seja JSON, exibe o texto bruto
        print(e)
except Exception as e:
    print(e)
# Requisição para obter o código-fonte do arquivo


# Dados de exemplo (substitua pelos dados reais do seu script)
errors = []
for path, details in components_msg.items():
    error_entry = {
        "file": path.replace(f'{PROJECT_KEY}:',''),
        "message": details[0],
        "severity": details[1],
        "line": details[2],
        "code": lines[details[2]]
    }
    errors.append(error_entry)
    print(error_entry)


# Criação do HTML
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

for index, error in enumerate(errors):
    html_content += f'''
        <div class="error" id="error{index + 1}">
            <h3 class="error-title">{error["file"]} <span class="toggle-icon"></span></h3>
            <div class="error-details">
                <p>Message: {error["message"]} at line {error["line"]}</p>
                <p>Severity: {error["severity"]}</p>
                <p>Line in Code: "{error["code"]}"</p>
            </div>
        </div>
    '''

# Fechando tags HTML
html_content += '''
    </div>
    <script>
        document.querySelectorAll('.error-title').forEach(title => {
            title.addEventListener('click', () => {
                const details = title.nextElementSibling;
                if (details.style.display === 'none' || details.style.display === '') {
                    details.style.display = 'block';
                } else {
                    details.style.display = 'none';
                }
            });
        });

        document.getElementById('toggleAll').addEventListener('click', () => {
            const allDetailsVisible = Array.from(document.querySelectorAll('.error-details')).every(details => details.style.display === 'block');
            document.querySelectorAll('.error-details').forEach(details => {
                details.style.display = allDetailsVisible ? 'none' : 'block';
            });
        });
    </script>
</body>
</html>
'''

# Salvar o HTML em um arquivo
path_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(path_dir, 'sonarqube-notification.html')

with open(file_path, 'w') as file:
    file.write(html_content)

print("HTML gerado com sucesso!")
