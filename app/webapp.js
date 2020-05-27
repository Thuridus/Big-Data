const dns = require('dns').promises;
const os = require('os')
const express = require('express')
const { addAsync } = require('@awaitjs/express');
const app = addAsync(express());
const mysqlx = require('@mysql/xdevapi');
const MemcachePlus = require('memcache-plus');
const router = express.Router();
const colors = require('colors');

// Months
const months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

//Connect to the memcached instances
let memcached = null
let memcachedServers = []

// Datenbank Konfiguration
const dbConfig = {
	user: 'root',
	password: 'mysecretpw',
	host: 'my-app-mysql-service',
	port: 33060,
	schema: 'mysqldb'
};

// Oberfläche einbinden
router.get('/', function(req,res){
	res.sendFile('/src/index.html');
});
app.use(express.static(__dirname));
app.use('/', router);
app.use(express.json());

var server = app.listen(8080, function () {
	var host = server.address().address
	var port = server.address().port
	console.log('- Express app listening at http://%s:%s', host, port)
});

// Aktualisieren der Memcached-Instancen (alle 5 sec)
async function getMemcachedServersFromDns() {
	let queryResult = await dns.lookup('my-memcached-service', { all: true });
	let servers = queryResult.map(el => el.address + ":11211")

	//Only create a new object if the server list has changed
	if (memcachedServers.sort().toString() !== servers.sort().toString()) {
		console.log("- Updated memcached server list to ", servers)
		memcachedServers = servers
		//Disconnect an existing client
		if (memcached)
			await memcached.disconnect()
		memcached = new MemcachePlus(memcachedServers);
	}
}

//Initially try to connect to the memcached servers, then each 5s update the list
getMemcachedServersFromDns()
setInterval(() => getMemcachedServersFromDns(), 5000)

//Get data from cache if a cache exists yet
async function getFromCache(key) {
	if(key.length > 250){
		console.log(`- Key: ${key} to long for a search in Memcache`);
		return null;
	}
	if (!memcached) {
		console.log(`- No memcached instance available, memcachedServers: ${memcachedServers}`)
		return null;
	}
	return await memcached.get(key);
}

//Get data from database
async function getFromDatabase(query, grouptyp) {
	let session = await mysqlx.getSession(dbConfig);
	console.log("- Executing query " + query);

	let res = await session.sql(query).execute();
	
	// Ergebnis verarbeiten
	var resultJSON = [], row;
	while (row = res.fetchOne()) {
		var element = {};
		if(grouptyp == "MONTH"){
			element.fieldname = months[row[1]] + " " + row[0];
		}else if(grouptyp == "WEEK"){
			element.fieldname = "KW " + row[1] + " " + row[0];
		}else{
			element.fieldname = row[1];
		}
        element.corona = row[2];
		element.dax = row[3];
		resultJSON.push(element);
	}
	console.log(resultJSON);
	return JSON.stringify(resultJSON);
}
// get countrys from DB
async function getCountrysFromDatabase(res) {
	let session = await mysqlx.getSession(dbConfig);
	let result = await session.sql("SELECT DISTINCT country FROM `infects` ORDER BY country;").execute();
	var resultJSON = [], row;
	while (row = result.fetchOne()) {
		resultJSON.push(row[0]);
	}
	res.send(resultJSON);
}

function send_response(response, data) {
	response.send(data);
}

app.post('/serverAbfrageStarten/', function (req, res) {
	console.log(`- Start DB Abfrage für ${req.body.sql}`.blue);
	console.log(`- Key der Abfrage ${req.body.key} (${req.body.key.length})`.blue);
	runRequest(req.body, res);
});

app.get('/getCountrys/', function (req, res){
	console.log("- Run country Query")
	getCountrysFromDatabase(res);
});


async function runRequest(json, response) {
	var sql = json.sql;
	var key = json.key;
	let cachedata = await getFromCache(key);

	if (cachedata) {
		console.log(`- Cache hit for key="${key}", cachedata = ${cachedata}`.green);
		response.send(cachedata);
	} else {
		console.log(`- Cache miss for key="${key}", querying database`.red);
		let data = await getFromDatabase(sql, json.grouptyp);
		if (data) {
			if(key.length <= 250){
				console.log(`- Storing data in cache`.green);
				if (memcached) await memcached.set(key, data, 300 /* seconds */);
			}
			send_response(response, data);
		} else {
			console.log(`- No data found!`.red);
			send_response(response, "No data found");
		}
	}
};