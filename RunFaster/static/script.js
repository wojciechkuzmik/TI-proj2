window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || 
window.msIndexedDB;
 
window.IDBTransaction = window.IDBTransaction || window.webkitIDBTransaction || 
window.msIDBTransaction;
window.IDBKeyRange = window.IDBKeyRange || 
window.webkitIDBKeyRange || window.msIDBKeyRange
 
if (!window.indexedDB) {
   window.alert("Your browser doesn't support a stable version of IndexedDB.")
}

var request = window.indexedDB.open("offlineDatabase", 1);
var db;

request.onerror = function(event) {
    console.log("error: ");
 };
 
 request.onsuccess = function(event) {
    db = request.result;
    console.log("success: "+ db);
 };

request.onupgradeneeded = function (event) {
	db = event.target.result;
	var store = db.createObjectStore("runs", { keyPath: "id", autoIncrement: true });
	store.createIndex("created", "created");
	store.createIndex("dist", "dist");
    store.createIndex("h", "h");
    store.createIndex("m", "m");
    store.createIndex("s", "s");

};


function offline(){
    var form = "<form>";
    form += "<h2>Czas</h2>";
    form += "<label for='hours'>Godziny</label>";
    form += "<input id = 'hours' name = 'hours' value = 0>";
    form += "<label for='minutes'>Minuty</label>";
    form += "<input id = 'minutes' name = 'minutes' value = 0>";
    form += "<label for='seconds'>Sekundy</label>";
    form += "<input id = 'seconds' name = 'seconds' value = 0>";
    form += "<br><label for='distance'>Dystans [km]</label>";
    form += "<input id = 'distance' name = 'distance' value = 0>";
    form += "<button type='button' onclick='add(this.form)'>Zapisz</button>";
    document.getElementById('offline_form').innerHTML = form;
}


function add(form) {
    var data = {};
    data.created = new Date(Date.now());
    data.dist = form.distance.value;
    data.h = form.hours.value;
    data.m = form.minutes.value;
    data.s = form.seconds.value;
    to_send = JSON.stringify(data);

    var request = db.transaction(["runs"], "readwrite")
    .objectStore("runs")
    .add(data);
    
    request.onsuccess = function(event) {
       alert("Pomyślnie dodano do bazy danych offline");
    };
    
    request.onerror = function(event) {
       alert("Error");
    }
 }


 function synchronize_data() {
	var counter = 0;
	var transaction = db.transaction("runs", "readwrite");
	var obj = transaction.objectStore("runs");
	obj.openCursor().onsuccess = function (event) {
		var cursor = event.target.result;
		if (cursor) {
			var data = {};
			data.dist = cursor.value.dist;
			data.h = cursor.value.h;
			data.m = cursor.value.m;
			data.s = cursor.value.s;
            to_send = JSON.stringify(data);
            
            $.post( "/synchronize", {
                javascript_data: to_send 
            });
			
			cursor.delete();
			counter += 1;
			cursor.continue();
		}
		else if (counter == 0) {
			alert("Brak danych offline.");
		}
	};
}
