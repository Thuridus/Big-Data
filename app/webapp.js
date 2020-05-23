const dns = require('dns').promises;
const os = require('os')
const express = require('express')
const { addAsync } = require('@awaitjs/express');
const app = addAsync(express());
const mysqlx = require('@mysql/xdevapi');
const MemcachePlus = require('memcache-plus');

//Connect to the memcached instances
let memcached = null
let memcachedServers = []

// Datenbank Konfiguration
const dbConfig = {
	user: 'root',
	password: 'mysecretpw',
	host: 'my-app-mysql-service',
	port: 33060,
	schema: 'sportsdb'
};

// Oberfläche einbinden
app.use(express.static('Interface'));
var server = app.listen(8080, function () {
	var host = server.address().address
	var port = server.address().port
	console.log('Express app listening at http://%s:%s', host, port)
});


// Aktualisieren der Memcached-Instancen (alle 5 sec)
async function getMemcachedServersFromDns() {
	let queryResult = await dns.lookup('my-memcached-service', { all: true })
	let servers = queryResult.map(el => el.address + ":11211")

	//Only create a new object if the server list has changed
	if (memcachedServers.sort().toString() !== servers.sort().toString()) {
		console.log("Updated memcached server list to ", servers)
		memcachedServers = servers
		//Disconnect an existing client
		if (memcached)
			await memcached.disconnect()
		memcached = new MemcachePlus(memcachedServers);
	}
}

//Initially try to connect to the memcached servers, then each 5s update the list
getMemcachedServersFromDns()
//setInterval(() => getMemcachedServersFromDns(), 5000)

//Get data from cache if a cache exists yet
async function getFromCache(key) {
	if (!memcached) {
		console.log(`No memcached instance available, memcachedServers = ${memcachedServers}`)
		return null;
	}
	return await memcached.get(key);
}

//Get data from database
async function getFromDatabase(query) {
	let session = await mysqlx.getSession(dbConfig);
	console.log("Executing query " + query);

	let res = await session.sql(query).execute();

	// TODO Hier wird das JSON erstellt
	let row = res.fetchOne();
	if (row) {
		console.log("Query result = ", row);
		return row[0];
	} else {
		return null;
	}
}

function send_response(response, data) {
	
}

app.post('/serverAbfrageStarten/', function (req, res) {
    if (req.method == 'POST') {
        var body = '';
        req.on('data', function (data) {
            body += data;
        });
        req.on('end', function () {
            runRequest(JSON.parse(body), res);
        });
    }
});

app.get('/getCountrys/', function (req, res){
    var country = ['Germany', 'Croatia', 'Austria', 'Italy', 'Switzerland'];
    res.send(country);
});


async function runRequest(json, response) {
	let sql = json.sql;
	let cachedata = await getFromCache(sql);

	if (cachedata) {
		console.log(`Cache hit for key=${key}, cachedata = ${cachedata}`);
		response.send(cachedata);
	} else {
		console.log(`Cache miss for key=${key}, querying database`);
		let data = await getFromDatabase(sql);
		if (data) {
			console.log(`Got data=${data}, storing in cache`);
			if (memcached)
				await memcached.set(sql, data, 30 /* seconds */);
			send_response(response, data);
		} else {
			console.log(`No data found!`);
			send_response(response, "No data found");
		}
	}
};