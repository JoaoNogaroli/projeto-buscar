var lista = [];
var str = '<ul>';
var lista_dois = [];
var a = 1;
var lista_nome = [];

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
                                        //lista_dois.push(snapshot.val().LinkDaVaga);
                                        //lista_nome.push(snapshot.val().NomeDaVaga);
                                        var snap_nome = snapshot.val().NomeDaVaga;
                                        var snap_link = snapshot.val().LinkDaVaga;
                                        var div = document.getElementById("slideContainer")

                                        
                                        

                                        var a_img = document.createElement('a');
                                        a_img.setAttribute = ('href');
                                        a_img.target = 'Starfall';
                                        a_img.href = snap_link;
                                        
                                        var img = document.createElement('img');
                                        img.src = '/static/redirect.png';
                                        img.className = 'imagem_resultado';
                                        a_img.appendChild(img)
                                        div.appendChild(a_img)

                                        var li_disc = document.createElement('h2');
                                        li_disc.textContent = snap_nome;
                                        li_disc.className = 'nome_resultado';
                                        div.appendChild(li_disc);

                                        var hr = document.createElement("hr");
                                        div.appendChild(hr);
                                    });
                                    });
                                });
                            
                            /*console.log("LISTADOIS: " + lista_dois)
                            lista_dois.forEach(function(item){
                                str += '<li>'+'<a hrf>'+ item +'</>' +'</li>';
                                console.log("ITEM: " + item);
                            });
                            str += '</ul>';
                            document.getElementById("slideContainer").innerHTML = str;
                            console.log("VALOR DE A: " + a)*/
                            clearInterval(interv);

                            console.log("Terminado")
                            document.getElementById("terminado").innerHTML = "Buscar Realizada com sucesso, pode clicar na lupa!";

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
            document.getElementById("atualize").innerHTML = "Se não apareceram resultados, atualize a página segurando o CTRL!"
            

        }
    }, 1000);
}

window.onload = function () {
    var fiveMinutes = 60 ,
        display = document.querySelector('#time');
    startTimer(fiveMinutes, display);
};

function image(){
    console.log("IMAGE");
    $("#" + "slideContainer").toggle(); 
    $("#" + "slideContainer_nome").toggle(); 

}