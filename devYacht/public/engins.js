

function myFunction() {
    var element = document.body;
    element.classList.toggle("dark-mode");
}

//https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/send
function sentEngineState(textRequest = "engineStates?stateRightEngine=on&stateLeftEngine=off") {
    textRequest = "engineStates?engineCmmand="+textRequest
    var xhr = new XMLHttpRequest();
    // xhr.open("POST", '/engineStates', true);

    xhr.open("POST", textRequest, true);

    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function () { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            // alert("TEST");
            // alert(xhr.response);
            var element = document.body;
            element.classList.toggle("dark-mode");
            // Request finished. Do processing here.
        }
    }
    xhr.send(textRequest);
    // xhr.send(new Int8Array()); 
    // xhr.send(document);
    window.onpopstate = function (e) {
        // if(e.state){
        //     document.getElementById("content").innerHTML = e.state.html;
        //     document.title = e.state.pageTitle;
        // }
    };
}


// function sentEngineState(targetServerRoute, engineName, engineState) {
//     textRequest = "engineStates?stateRightEngine=on&stateLeftEngine=off"
//     var xhr = new XMLHttpRequest();
//     // xhr.open("POST", '/engineStates', true);

//     xhr.open("POST", textRequest, true);

//     //Send the proper header information along with the request
//     xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

//     xhr.onreadystatechange = function () { // Call a function when the state changes.
//         if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
//             // alert("TEST");
//             // alert(xhr.response);
//             var element = document.body;
//             element.classList.toggle("dark-mode");
//             // Request finished. Do processing here.
//         }
//     }
//     xhr.send(textRequest);
//     // xhr.send(new Int8Array()); 
//     // xhr.send(document);
//     window.onpopstate = function (e) {
//         // if(e.state){
//         //     document.getElementById("content").innerHTML = e.state.html;
//         //     document.title = e.state.pageTitle;
//         // }
//     };
// }



function onclick(e) {

    var printBlock = document.getElementById("printBlock");
    var stateOfEngine = e.target.value;
    // e.style.color = "blue";
    printBlock.textContent = "The current state of the left engine is: " + stateOfEngine;
    sentEngineState(textRequest = e.target.value);
    return stateOfEngine;

}

function engineListner(EngineHtmlClass) {
    for (var i = 0; i < EngineHtmlClass.languages.length; i++) {
        stateOfEngine = EngineHtmlClass.languages[i].addEventListener("click", onclick);
    }
}
