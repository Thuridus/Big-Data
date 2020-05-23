

var $$ = Dom7;
var app = new Framework7({
  // App root element
  root: '#app',
  // App Name
  name: 'Big Data',
  // App id
  id: 'de.famlovric.Big-Data',
  // Enable swipe panel
  panel: {
    swipe: 'left',
  },
});


var calendarRange = app.calendar.create({
  inputEl: '#calendar-range',
  dateFormat: {
    month: '2-digit',
    day: '2-digit',
    year: 'numeric'
  },
  rangePicker: true
});

app.toggle.create({
  el: '.toggleRelative',
  on: {
    change: function (e) {
      $$("input[name='toggleRelative']").val(e.checked);
    }
  }
});
app.toggle.create({
  el: '.toggleTode',
  on: {
    change: function (e) {
      $$("input[name='toggleTode']").val(e.checked);
    }
  }
})


app.request.get('/getCountrys/', function (data){
  var json = JSON.parse(data);
  for(var i in json){
    var element = document.createElement("option");
    element.setAttribute("value", `'${json[i]}'`);
    element.innerHTML = json[i];
    $$("select[name='country']").append(element);
  }
});


$$(".convert-form-to-data").on("click", function () {
  var content = app.form.convertToData('#my-form');
  if (content.dateRange.indexOf("-") < 0) {
    // NULL-Prüfung für den Datumsbereich durchführen
    alert("Bitte einen Datumsbereich auswählen");
    return;
  } else if (content.country.length == 0) {
    // NULL-Prüfung für das Land durchführen
    alert("Mindestens ein Vergleichsland auswählen");
    return;
  } else {
    // Ermitteln des Start- und End-Datums
    var startDate = new Date(calendarRange.value[0]);
    var endDate = new Date(calendarRange.value[1]);
    content.startDate = startDate.getFullYear() + "-" + (startDate.getMonth() + 1) + "-" + startDate.getDate();
    content.endDate = endDate.getFullYear() + "-" + (endDate.getMonth() + 1) + "-" + endDate.getDate();

    // Ermittlung des Corona Selektions-Typs
    var coronaTyp = $$("input[name='radio-coronaTyp'][checked]").prop("checked") ? "death" : "cases";

    // Array der betrachten Länder vorbereiten
    var countrys = Array(content.country).toString();

    // Prüfen der Zeitspanne > 4 Monate | Dann Umwandeln in Tage und prüfen ob mehr als 4 Wochen = 28 Tage 
    if ((endDate.getFullYear() - startDate.getFullYear()) + (endDate.getMonth() - startDate.getMonth()) > 5) {
      content.selectRange = "month";
      content.sql = `SELECT MONTH(date), SUM(${coronaTyp}) FROM infects WHERE date BETWEEN '${content.startDate}' AND '${content.endDate}' AND country IN (${countrys}) GROUP BY MONTH(date);`;
    } else if ((endDate - startDate) / 86400000 >= 28) {
      content.selectRange = "week";
      content.sql = `SELECT WEEK(date), SUM(${coronaTyp}) FROM infects WHERE date BETWEEN '${content.startDate}' AND '${content.endDate}' AND country IN (${countrys}) GROUP BY WEEK(date);`;
    } else {
      content.selectRange = "day";
      content.sql = `SELECT date, ${coronaTyp} FROM infects WHERE date BETWEEN '${content.startDate}' AND '${content.endDate}' AND country IN (${countrys});`;
    }

    
    app.request.postJSON('/serverAbfrageStarten/', content, function (data) {
      data = json;
      $$("#zeitstrahl").html("");
      var minValueDax = data[0].dax;
      var maxValueDax = data[0].dax;
      var minValueCorona = data[0].corona;
      var maxValueCorona = data[0].corona;
      for (var i in data) {
        // Monate eintragen
        var spanElement = document.createElement("span");
        spanElement.innerHTML = data[i].fieldname;
        $$("#zeitstrahl").append(spanElement);
        // Skalenwerte vorbereiten --> Min & Max Werte ermitteln
        if (data[i].dax > maxValueDax) maxValueDax = data[i].dax;
        if (data[i].dax < minValueDax) minValueDax = data[i].dax;
        if (data[i].corona > maxValueCorona) maxValueCorona = data[i].corona;
        if (data[i].corona < minValueCorona) minValueCorona = data[i].corona;

      }
      $$("#zeitstrahl span").css("line-height", 800 / data.length + "px");

      // Skalen einrichten
      $$("#daxMax").html(maxValueDax);
      $$("#daxMin").html(minValueDax);
      $$("#coronaMax").html(maxValueCorona);
      $$("#coronaMin").html(minValueCorona);

      // Grafen zeichen
      var skalierungDax = 125 / (maxValueDax - minValueDax);
      var skalierungCorona = 125 / (maxValueCorona - minValueCorona);
      var skalierungGraf = 800 / data.length;
      
      var daxGraf = "";
      var coronaGraf = "";
      for (var i = 0; i < data.length; i++) {
        daxGraf += "L" + ((i + 0.5) * skalierungGraf) + " " + (150 - ((data[i].dax - minValueDax) * skalierungDax));
        coronaGraf += "L" + ((i + 0.5) * skalierungGraf) + " " + (150 - ((data[i].corona - minValueCorona) * skalierungCorona));
      }
      $$("#daxGraf").attr("d", daxGraf.replace("L", "M"));
      $$("#coronaGraf").attr("d", coronaGraf.replace("L", "M"));

    }, (e) => console.log(e));
  }
});