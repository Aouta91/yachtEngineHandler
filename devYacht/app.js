// получаем модуль Express
const express = require("express");
const http = require("http");
const fs = require("fs");
const Emitter = require("events");
const EventEmitter = require("events");


function appendControlCommands(direction){
    fs.appendFileSync("IOstreams/out", direction+"\n");
    console.log(direction);
};

// создаем приложение
const app = express();


app.use(function(request, response, next){
     
    let now = new Date();
    let hour = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();
    let data = `${hour}:${minutes}:${seconds} ${request.method} ${request.url} ${request.get("user-agent")}`;
    console.log(data);
    fs.appendFile("server.log", data + "\n", function(){});
    next();
});




app.use("/static", express.static(__dirname + "/public"));


// app.use("/engineState*", function(request, response, next){
app.use("/", function(request, response, next){
//    http://localhost:3000/engineStates?stateRightEngine=on&stateLeftEngine=on
  //  let id = request.query.id;
    //let userName = request.query.name;

    let stateRightEngine  = request.query.stateRightEngine;
    let stateLeftEngine = request.query.stateLeftEngine;
    // response.send("<h1>Информация</h1>");
    
    // fs.readFile("sites/engineStates.html", "utf8", function(error, data){
    
    fs.readFile("public/index.html", "utf8", function(error, data){
        let header = "Главная страница";

        // data = data.replace("{header}", header);
        data = data.replace("{header}", header).replace("{stateRightEngine}", stateRightEngine).replace("{stateLeftEngine}", stateLeftEngine);
        let enginsStateJson = JSON.stringify({stateRightEngine: stateRightEngine, stateLeftEngine: stateLeftEngine});
        response.send(data);
        // response.send(enginsStateJson);
    });
    console.log( stateRightEngine  +stateLeftEngine) ;
    appendControlCommands(stateRightEngine  +stateLeftEngine)

});


app.use("/statesHandles", function(request, response, next){
    //    http://localhost:3000/engineStates?stateRightEngine=on&stateLeftEngine=on
      //  let id = request.query.id;
        //let userName = request.query.name;
    
        let stateRightEngine  = request.query.stateRightEngine;
        let stateLeftEngine = request.query.stateLeftEngine;
        // response.send("<h1>Информация</h1>");
        
        // fs.readFile("sites/engineStates.html", "utf8", function(error, data){
        
        fs.readFile("public/index.html", "utf8", function(error, data){
            let header = "Главная страница";
    
            // data = data.replace("{header}", header);
            data = data.replace("{header}", header).replace("{stateRightEngine}", stateRightEngine).replace("{stateLeftEngine}", stateLeftEngine);
            let enginsStateJson = JSON.stringify({stateRightEngine: stateRightEngine, stateLeftEngine: stateLeftEngine});
            response.send(data);
            // response.send(enginsStateJson);
        });
        console.log( stateRightEngine  +stateLeftEngine) ;
        appendControlCommands(stateRightEngine  +stateLeftEngine)
        // next();
    // 
        // console.log( request.query.stateRightEngine);
        // response.send(data);
    
    });
    



// начинаем прослушивание подключений на 3000 порту
// let message = "Hello World!";

app.listen(3000, "127.0.0.1",()=>{
// app.listen(3000, "192.168.198.148",()=>{
    console.log("Сервер начал прослушивание запросов");
});







 
