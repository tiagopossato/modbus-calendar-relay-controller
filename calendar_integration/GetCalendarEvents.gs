function listEvents() {
  // Substitua 'CALENDAR_ID' pelo ID do seu calendário
  var calendarId = 'CALENDAR_ID';
  
  // Obter o calendário
  var calendar = CalendarApp.getCalendarById(calendarId);
  
  // Definir o intervalo de tempo para o dia atual
  var now = new Date();
  var startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0);
  var endOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59);
  
  // Ler os eventos do dia atual
  var events = calendar.getEvents(startOfDay, endOfDay);
  
  // Filtrar eventos que estão ocorrendo exatamente agora
  var hasCurrentEvent = events.some(event => {
    var start = event.getStartTime();
    var end = event.getEndTime();
    return start <= now && now <= end;
  });
  
  return hasCurrentEvent;
}

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({ "hasEventNow": listEvents() }))
    .setMimeType(ContentService.MimeType.JSON);
}
