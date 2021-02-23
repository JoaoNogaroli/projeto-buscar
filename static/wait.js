var lista = [];
var str = '<ul>';
var lista_dois = [];
var a = 1;

firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
         
            var user_uid = firebase.auth().currentUser.uid;
            console.log("TESTE atualiza");
            var database = firebase.database();
            console.log("ALOO: "+ user_uid);
            var database = firebase.database();
            console.log("TAMANHO LISTA 1:" + lista.length)
     
                if (a =1){
                    var interv = setInterval(function repetir() {

                        if(lista.length==0){
                            database.ref('Users').child(user_uid).child('Pesquisa').child('Lista_resultados').on('value', function(snapshot){
                                snapshot.forEach(function(data) {  
                                    database.ref('Users').child(user_uid).child('Pesquisa').child('Lista_resultados').child(data.key).on('value', function(snapshot){
                                        lista.push(snapshot.val().LinkDaVaga);
                                        /*console.log(lista)*/
                                        
                                    });
                                    });
                                });
                                console.log("TAMANHO LISTA :" + lista.length)
                        }else{
                            a = 2
                            console.log("FEITO");
                            database.ref('Users').child(user_uid).child('Pesquisa').child('Lista_resultados').on('value', function(snapshot){
                                snapshot.forEach(function(data) {  
                                    database.ref('Users').child(user_uid).child('Pesquisa').child('Lista_resultados').child(data.key).on('value', function(snapshot){
                                        lista_dois.push(snapshot.val().LinkDaVaga);
                                        
                                    });
                                    });
                                });
                            console.log("LISTADOIS: " + lista_dois)
                            lista_dois.forEach(function(item){
                                str += '<li>'+'<a hrf>'+ item +'</>' +'</li>';
                                console.log("ITEM: " + item);
                            });
                            str += '</ul>';
                            document.getElementById("slideContainer").innerHTML = str;
                            console.log("VALOR DE A: " + a)
                            clearInterval(interv);

                            console.log("Terminado")
                             
                        }
                        
                    }, 10000) ;
                   
                }else{
                    console.log("TERMINADO")
                }
                    
    };
});



console.log("TERCEIRA")

function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration*0;
        }
    }, 1000);
}

window.onload = function () {
    var fiveMinutes = 60 ,
        display = document.querySelector('#time');
    startTimer(fiveMinutes, display);
};