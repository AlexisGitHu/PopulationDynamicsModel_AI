$(function() {
  	$('#inicio_ajax').on('click', function(e) {
		ajaxCall();
	})
})

$(function() {
  	$('#cambio').on('click', function(e) {
		ajaxCall();
	})
})
let direccion = 'http://localhost:5000/prueba1';
var data = {"claveA":"parametroB"};
function ajaxCall() {
    // console.log("hola");
    var request = $.ajax({
        type: 'POST',
        data: data,
        url: direccion,
        success: function(datos) {
        	if(datos == "http://localhost:5000/login"){
        		window.location.replace(datos);
        	}else if (datos == "base"){
        		window.location.replace("C:/Users/claud/OneDrive/Escritorio/ProyectosIII/PopulationDynamicsModel_AI/Code/Servidor/templates/base.html");
        	}
        	
        }
    })
}


