

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
    // Zusammenstellen Key für Memcached-Server
    var key = "";
    // Ermitteln des Start- und End-Datums
    var startDate = new Date(calendarRange.value[0]);
    var endDate = new Date(calendarRange.value[1]);
    content.startDate = startDate.getFullYear() + "-" + (startDate.getMonth() + 1) + "-" + startDate.getDate();
    content.endDate = endDate.getFullYear() + "-" + (endDate.getMonth() + 1) + "-" + endDate.getDate();
    key += content.startDate + "/" + content.endDate + "/";


    // Ermittlung des Corona Selektions-Typs
    var coronaTyp = $$("input[name='radio-coronaTyp'][checked]").prop("checked") ? "deaths" : "cases";
    // Prüfen auf relative Veränderung
    var coronaTyp = $$("input[name='toggleRelative']").prop("checked") ? coronaTyp + "_rel_diff" : coronaTyp;
    // Hinzufügen CoronaTyp zum key
    key += coronaTyp + "/";
    // Array der betrachten Länder vorbereiten
    var countrys = Array(content.country).toString();
    // Hinzufügen Län der zum key
    key += countrys + "/";

    // Prüfen der Zeitspanne > 4 Monate | Dann Umwandeln in Tage und prüfen ob mehr als 4 Wochen = 28 Tage 
    var grouptyp = "";
    if ((endDate.getFullYear() - startDate.getFullYear()) + (endDate.getMonth() - startDate.getMonth()) > 4) {
      grouptyp = "MONTH";
      key += "month";
    } else if ((endDate - startDate) / 86400000 >= 28) {
      grouptyp = "WEEK";
      key += "month";
    }else{
      key += "day";
    }

    var sql = `SELECT YEAR(dax.date) as year, ${grouptyp}(dax.date) as field, sum(infects.${coronaTyp}) as corona, sum(dax.diff) as dax FROM infects INNER JOIN dax ON infects.date = dax.date WHERE dax.date BETWEEN '${content.startDate}' AND '${content.endDate}' AND country IN (${countrys}) GROUP BY YEAR(dax.date), ${grouptyp}(dax.date) ORDER BY YEAR(dax.date), MONTH(dax.date);`;
    
    app.request.postJSON('/serverAbfrageStarten/', {"sql": sql, "key": key, "grouptyp": grouptyp}, function (data) {
      $$("#zeitstrahl").html("");
      var daxValue = 0;
      var minValueDax = 0;
      var maxValueDax = 0;
      var minValueCorona = data[0].corona;
      var maxValueCorona = data[0].corona;
      for (var i in data) {
        // Monate eintragen
        var spanElement = document.createElement("span");
        spanElement.innerHTML = data[i].fieldname;
        $$("#zeitstrahl").append(spanElement);

        // Skalenwerte vorbereiten --> Min & Max Werte ermitteln
        daxValue += data[i].dax;
        if (daxValue > maxValueDax) maxValueDax = daxValue;
        if (daxValue < minValueDax) minValueDax = daxValue;
        if (data[i].corona > maxValueCorona) maxValueCorona = data[i].corona;
        if (data[i].corona < minValueCorona) minValueCorona = data[i].corona;

      }

      // Skalen runden
      minValueDax = Math.floor(minValueDax / 10) * 10
      maxValueDax = Math.ceil(maxValueDax / 10) * 10

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
      
      var dax_Y = 25 + (skalierungDax * maxValueDax);
      var daxGraf = "";
      var coronaGraf = "";
      for (var i = 0; i < data.length; i++) {
        dax_Y -= (data[i].dax * skalierungDax);
        daxGraf += "L" + ((i + 0.5) * skalierungGraf) + " " + (dax_Y);
        coronaGraf += "L" + ((i + 0.5) * skalierungGraf) + " " + (150 - ((data[i].corona - minValueCorona) * skalierungCorona));
      }
      $$("#daxGraf").attr("d", daxGraf.replace("L", "M"));
      $$("#coronaGraf").attr("d", coronaGraf.replace("L", "M"));

    }, (e) => console.log(e));
    
  }
});