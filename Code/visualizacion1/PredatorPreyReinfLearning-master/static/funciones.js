//David García Lleyda MAIS 3A


//Construir el Ajax
const request = new XMLHttpRequest();

// request.open(TIPO, URL) 
// tipo : 'GET', 'POST', 'PUT', 'DELETE'
request.open('GET','https://jsonplaceholder.typicode.com/photos') //Abrir comunicacion (Handshake)
request.send(); //Leyendo el dato

// request.onreadystatechange = ()=>{};  Funcion anonima asociada al onreadystatechange
request.onreadystatechange = (e)=>
							{
								if(request.readyState === 4)
								{
									const fotos = JSON.parse(request.responseText);
									var nf;
									// fotos.forEach(FUNCION)
									fotos.forEach
									(
										(foto) => 
										{
											$("#table_body").append('<tr id="nf"> </tr>');

											nf = $("#nf");

											nf.append('<td> '+ foto['albumId'] +' </td>');
											nf.append('<td> '+ foto['id'] +' </td>');
											nf.append('<td> '+ foto['title'] +' </td>');
											nf.append('<td> <img src="'+ foto['thumbnailUrl'] +'"></img> </td>');
											nf.removeAttr("id");
										}
									);

								}
							};