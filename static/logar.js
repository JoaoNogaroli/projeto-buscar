var btnLogin = document.getElementById('btnLogin');
var email = document.getElementById('email');
var password = document.getElementById('password');


       
btnLogin.addEventListener('click', function(){

   firebase.auth().signInWithEmailAndPassword(email.value, password.value).then(function(result){
      window.alert("Bem Vindo:  " + email.value)
      window.location.href = "http://127.0.0.1:5000/segundapag"      
      
  }).catch(function(error) {
      // Handle Errors here.

      
      var errorCode = error.code;
      var errorMessage = error.message;
      alert("ERror")
      // ...
    });
});