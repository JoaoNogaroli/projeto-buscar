firebase.auth().onAuthStateChanged(function(user) {

    if (user) {
      var usuario = firebase.auth().currentUser;

      
      document.getElementById("input_email").value = usuario.email; 
      document.getElementById("user_uid").value = firebase.auth().currentUser.uid; 
      document.getElementById("user_uid_dois").value = firebase.auth().currentUser.uid; 


      // User is signed in.
     

    } else {
      // No user is signed in.
    }
  });

  

