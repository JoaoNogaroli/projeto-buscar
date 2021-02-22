var database = firebase.database();


var btnCadastrar = document.getElementById('btnCadastrar');
var cad_email = document.getElementById('cad_email');
var cad_password = document.getElementById('cad_password');

$('#btnCadastrar').click(function(){
    firebase.auth().createUserWithEmailAndPassword(cad_email.value, cad_password.value)
    .then((user) => {
      // Signed in
      window.alert("CADASTRO REALIZADO COM SUCESSO"+ "\n" +"\n Obrigado!")
      var userUid = firebase.auth().currentUser.uid;
      var email_user = firebase.auth().currentUser.email

      database.ref('Users').child(userUid).set({
        'email': email_user,
        'userUid': userUid,        
        'nome': '',
        
    })

      // ...
    })
    .catch((error) => {
      window.alert("Confira seus dados!")
      var errorCode = error.code;
      var errorMessage = error.message;
      // ..
    });
    cad_email.value="";
    cad_password.value="";  
  
});