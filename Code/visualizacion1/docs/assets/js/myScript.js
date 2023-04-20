
paper.install(window);
window.onload = function() {
    paper.setup('myCanvas');

    let inicio_ajax = document.getElementById("inicio_ajax");
    console.log(inicio_ajax);
    inicio_ajax.onclick = ajaxCall;
    var j;
    var id = [];
    var dict = {};
    var vector;
    var velocidad=0;
    var x_relativa;
    var y_relativa;
    var width = $("#myCanvas").width();
    var height = $("#myCanvas").height();

    let cambiar_velocidad = document.getElementById("cambiar_velocidad");
    cambiar_velocidad.onclick = cambiar;
    function cambiar(evento,) {
        velocidad = document.getElementById("velocidad").value;
    };

    function ajaxCall() {
        var request = $.ajax({
            type: 'GET',
            url: 'http://localhost:5000/muestra/mesa/0',
            success: function(data) {
                console.log(data);
                if(data.length > 0){
                    $("#inicio_ajax").css("visibility","hidden");
                    console.log("entra en el if");
                    console.log(data);
                    if(velocidad == 0){
                        velocidad = 10;
                    }
                    var j = 0;
                    for(var i=0;i<data[j].info.length;i++){
                        if(data[j].info[i].Sprite == "lobo.png"){
                            var animal = "lobo";
                        }else if(data[j].info[i].Sprite == "conejo.png"){
                            var animal = "conejo";
                        }else if(data[j].info[i].Sprite == "cesped.png"){
                            var animal = "cesped";
                        }
                        if(!id.includes(data[j].info[i].ID)){
                            x_relativa = data[j].info[i].Position[0]*(width/10);
                            y_relativa = data[j].info[i].Position[1]*(height/10);
                            destination = new Point(x_relativa,y_relativa);
                            eval('var ' + animal + data[j].info[i].ID + '= new Raster({ source: "'+ data[j].info[i].Sprite +'", position: '+ destination +'});');                                
                            dict[animal + data[j].info[i].ID] = eval(animal + data[j].info[i].ID);
                            id.push(data[j].info[i].ID);
                            console.log(animal + data[j].info[i].ID);
                        }
                    }
                    let inicio = document.getElementById("inicio");
                    inicio.onclick = iniciar;
                    function iniciar(evento,) {
                        j++;
                        if (j >= data.length){ajaxCall()}
                        else{
                            console.log("step" + j);
                            for(var i=0;i<data[j].info.length;i++){
                                if(data[j].info[i].Sprite == "lobo.png"){
                                    var animal = "lobo";
                                }else if(data[j].info[i].Sprite == "conejo.png"){
                                    var animal = "conejo";
                                }else if(data[j].info[i].Sprite == "cesped.png"){
                                    var animal = "cesped";
                                }
                                if(!id.includes(data[j].info[i].ID)){
                                    x_relativa = data[j].info[i].Position[0]*(width/13);
                                    y_relativa = data[j].info[i].Position[1]*(height/13);
                                    destination = new Point(x_relativa,y_relativa);
                                    eval('var ' + animal + data[j].info[i].ID + '= new Raster({ source: "'+ data[j].info[i].Sprite +'", position: ' + destination  + '});');                                
                                    dict[animal + data[j].info[i].ID] = eval(animal + data[j].info[i].ID);
                                    id.push(data[j].info[i].ID);
                                    console.log(animal + data[j].info[i].ID);
                                }else{
                                    console.log(animal + data[j].info[i].ID + "" + data[j].info[i].Alive);
                                    if(data[j].info[i].Alive == "False"){
                                        console.log("muere" + animal + data[j].info[i].ID);
                                        eval(animal + data[j].info[i].ID).visible = false;
                                    }
                                }
                            }
                            var destination;
                            console.log("prueba");
                            console.log(j);
                            view.onFrame = function(event){
                                console.log("***");
                                console.log(j);
                                console.log(data.length);
                                console.log("***");
                                if(j >= data.length){
                                    return;
                                }
                                for(var i=0;i<data[j].info.length;i++){
                                    if(data[j].info[i].Sprite == "lobo.png"){
                                        var animal = "lobo";
                                    }else if(data[j].info[i].Sprite == "conejo.png"){
                                        var animal = "conejo";
                                    }else if(data[j].info[i].Sprite == "cesped.png"){
                                        var animal = "cesped";
                                    }
                                    
                                    if(id.includes(data[j].info[i].ID)){ 
                                        x_relativa = data[j].info[i].Position[0]*(width/13);
                                        y_relativa = data[j].info[i].Position[1]*(height/13);
                                        destination = new Point(x_relativa,y_relativa);
                                        vector = destination.subtract(dict[animal + data[j].info[i].ID].position);
                                        dict[animal + data[j].info[i].ID].position = dict[animal + data[j].info[i].ID].position.add(vector.divide(velocidad)); //vector.divide(velocidad)
 
                                    }
                                }       
                            };
                        }//fin del else
                    }//fin del iniciar
                }//fin del if data > 0
                console.log("ha salido del if");
            }//fin del success
        })
    }

    Raster.prototype.rescale = function(width, height) {
        this.scale(width / this.width, height / this.height);
    };

   
}