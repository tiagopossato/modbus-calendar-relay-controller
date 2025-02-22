# IMPLANTAÇÃO

O acesso ao Google calendar é feito indiretamente usando um script do Google. Isso simplifica o acesso, pois entrega uma API que retorna um objeto JSON com o atributo booleano hasEventNow, indicando se tem evento ocorrendo no instante do acesso.

Passo a passo para implantação da API de acesso ao Google Calendar:
 - Para implantar é preciso criar uma agenda específica para cada relé
 - Criar um script do Apps Script
 - Colar o conteúdo do arquivo GetCalendarEvents.gs
 - Colar o ID da agenda na variável CALENDAR_ID
 - Implantar > Nova Implantação
   - Executar como 'Eu'
   - Quem pode acessar: Qualquer pessoa
- Implantar
- Autorizar acesso. 
   - Se o Google mostrar uma mensagem diendo que não pode verificar o app, clique em Advanced (avançado) e no útimo link que aparece para autorizar o acesso. Por fim clique em Allow (permitir)
 - Copiar a URL do App da Web e usar com a função has_event. Essa função retorna True se tiver evento na agenda no instante em ela for chamada ou False se não tiver evento

A execução é relativamente lenta, em torno de 1 segundo, mas esse tempo de resposta não interfere na usabilidade da aplicação.

# Compartilhamento da agenda

Você pode compartilhar a agenda com quem quiser e gerenciar isso nas configurações da agenda.

# Uso da agenda

Para usar basta criar um evento na agenda específica, configurando o horário de início e fim corretamente.