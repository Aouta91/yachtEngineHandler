// получаем модуль Express
const express = require("express");
const http = require("http");
const fs = require("fs");
const Emitter = require("events");
const EventEmitter = require("events");



function initEvent(){
    let emitter = new Emitter();
    let eventName = "turner";
    let directionCmd ="Right";


    // emitter.emit(eventName, "Привет пир!");

    console.log("Right");
    emitter.on(eventName, function(directionCmd){
        appendControlCommands(direction = directionCmd);
        // appendControlCommands(directionCmd = "Left");
        // console.log("Hello all!");
        console.log("Привет!, right");
    });
    
    // emitter.on(eventName, function(){
    //     console.log("Привет!");
    // });
    
    emitter.emit(eventName, "Test");
};







function writeControlCommands(){
    fs.writeFile("hello.txt", "Hello мир!", function(error){
 
        if(error) throw error; // если возникла ошибка
        console.log("Асинхронная запись файла завершена. Содержимое файла:");
        let data = fs.readFileSync("hello.txt", "utf8");
        console.log(data);  // выводим считанные данные
    });
};

function appendControlCommands(direction){
    fs.appendFileSync("hello.txt", direction);
    console.log(direction);
};





// создаем приложение
const app = express();

// app.get("/static", express.static(__dirname + "/public"));
// app.get('engins.js', function (req, res) {
//     fs.readFile("public/engins.js", "utf8", function(error, data){
//         // let header = "Главная страница";

//         // // data = data.replace("{header}", header);
//         // data = data.replace("{header}", header).replace("{stateRightEngine}", stateRightEngine).replace("{stateLeftEngine}", stateLeftEngine);
//         // let enginsStateJson = JSON.stringify({stateRightEngine: stateRightEngine, stateLeftEngine: stateLeftEngine});
//         response.send(data);
//         // response.send(enginsStateJson);
//     });
//   })



//write to log requests
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
    // next();
// 
    // console.log( request.query.stateRightEngine);
    // response.send(data);

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

// app.listen(3000, "127.0.0.1",()=>{
app.listen(3000, "192.168.198.147",()=>{
    console.log("Сервер начал прослушивание запросов");
});







 
