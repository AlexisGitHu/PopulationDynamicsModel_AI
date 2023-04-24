var var_ajaxCall = null;

var num_cols_repartir = 10;
var num_filas_repartir = 10;

paper.install(window);
window.onload = function() {
    mi_canvas = $("#myCanvas");
    paper.setup('myCanvas');

    // let inicio_ajax = document.getElementById("inicio_ajax");
    // console.log(inicio_ajax);
    // inicio_ajax.onclick = var_ajaxCall["ajaxCall"]();
    var j;
    var id = [];
    var dict = {};
    var vector;
    var velocidad=0;
    var x_relativa;
    var y_relativa;

    // var width_inicial = $("#myCanvas").width();
    // var height_inicial = $("#myCanvas").height();
    
    // var margin_left = parseInt($("#myCanvas").css("margin-left").replace("px", ""));
    // var border = parseInt($("#myCanvas").css("border-left-width").replace("px", ""));
    // console.log(margin_left);
    // console.log(border);

    var margin_left_deseado = $(window).width()/20;
    var margin_top_deseado = $(window).height()/11;
    var margin_bottom_deseado = $(window).height()/11;

    var height_deseado = $(window).height()*8/11;
    var width_deseado = height_deseado*3/2;
    
    // console.log(width_inicial);
    // console.log(width_deseado);
    // console.log(width_inicial/width_deseado);

    // var proporcion_width = width_inicial/width_deseado;
    // var proporcion_height = height_inicial/height_deseado;
    
    $("#myCanvas").width(width_deseado);
    $("#myCanvas").height(height_deseado);

    // width_deseado = $(window).width()/2;
    // height_deseado = width_deseado;
    // console.log(width_deseado);
    
    // Seteamos el size que queremos para el canvas
    paper.view.viewSize = new Size(width_deseado,height_deseado);
    
    // // paper.view.viewSize = ;
    // console.log("****************");
    // console.log(width_deseado);
    // console.log(paper.view.viewSize.width);
    // console.log("****************");

    // Seteamos un offset para ver bien todos los agentes
    paper.view.translate(new Point(width_deseado/(num_cols_repartir*2),height_deseado/(num_filas_repartir*2)));
    
    
    // paper.view.scale(0.2);


    $("#myCanvas").css("margin-left", margin_left_deseado);
    $("#myCanvas").css("margin-top", margin_top_deseado);
    $("#myCanvas").css("margin-bottom", margin_bottom_deseado);
    
    var width = $("#myCanvas").width();
    var height = $("#myCanvas").height();
    
    // console.log(height);
    // console.log(width);

    // let cambiar_velocidad = document.getElementById("cambiar_velocidad");
    // cambiar_velocidad.onclick = cambiar;
    // function cambiar(evento,) {
    //     velocidad = document.getElementById("velocidad").value;
    // };

    var_ajaxCall = function ajaxCall() {
        // console.log("hola");
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
                    console.log("Hay este numero de elementos");
                    console.log(data[j].info.length);
                    for(var i=0;i<data[j].info.length;i++){
                        if(data[j].info[i].Sprite == "lobo.png"){
                            var animal = "lobo";
                        }else if(data[j].info[i].Sprite == "conejo.png"){
                            var animal = "conejo";
                        }else if(data[j].info[i].Sprite == "cesped.png"){
                            var animal = "cesped";
                        }
                        if(!id.includes(data[j].info[i].ID)){
                            x_relativa = data[j].info[i].Position[0]*(width/num_cols_repartir);
                            y_relativa = data[j].info[i].Position[1]*(height/num_filas_repartir);
                            // x_relativa = data[j].info[i].Position[0]*((width+2*border)*proporcion_width/10)+2*border;
                            // y_relativa = data[j].info[i].Position[1]*((height+2*border)*proporcion_height/10)+2*border;
                            destination = new Point(x_relativa,y_relativa);
                            // David
                            // console.log(destination);
                            // Fin David
                            // eval('var ' + animal + data[j].info[i].ID + '= new Raster({ source: "'+ data[j].info[i].Sprite +'"});');                     
                            eval('var ' + animal + data[j].info[i].ID + '= new Raster({ source: "'+ data[j].info[i].Sprite +'", position: '+ destination +'});');
                            dict[animal + data[j].info[i].ID] = eval(animal + data[j].info[i].ID);
                            // Prueba David //
                            // var scale = (width / dict[animal + data[j].info[i].ID].bounds.width) * 0.07;
                            var scale = 1/5;
                            // console.log("***********************************************");
                            // console.log(scale);
                            // console.log(dict[animal + data[j].info[i].ID]);
                            // console.log(dict[animal + data[j].info[i].ID].bounds);
                            // console.log(dict[animal + data[j].info[i].ID].bounds.width);
                            // console.log("***********************************************");
                            dict[animal + data[j].info[i].ID].scale(scale);
                            // dict[animal + data[j].info[i].ID].position = destination;
                            // dict[animal + data[j].info[i].ID].setPosition(destination);
                            dict[animal + data[j].info[i].ID].visible = true;
                            // console.log(dict[animal + data[j].info[i].ID]);
                            // Fin Prueba David //


                            id.push(data[j].info[i].ID);
                            // console.log(animal + data[j].info[i].ID);
                        }
                    }
                    let inicio = document.getElementById("btn_siguiente");
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

                                    // x_relativa = data[j].info[i].Position[0]*((width+2*border)*proporcion_width/10)+2*border;
                                    // y_relativa = data[j].info[i].Position[1]*((height+2*border)*proporcion_height/10)+2*border;
                                    x_relativa = data[j].info[i].Position[0]*(width/num_cols_repartir);
                                    y_relativa = data[j].info[i].Position[1]*(height/num_filas_repartir);

                                    destination = new Point(x_relativa,y_relativa);
                                    // David
                                    // console.log(destination);
                                    // Fin David
                                    eval('var ' + animal + data[j].info[i].ID + '= new Raster({ source: "'+ data[j].info[i].Sprite +'", position: ' + destination + '});');                                
                                    dict[animal + data[j].info[i].ID] = eval(animal + data[j].info[i].ID);

                                    // Prueba David //
                                    var scale = 1/5;
                                    // console.log("***********************************************");
                                    // console.log(scale);
                                    // console.log(dict[animal + data[j].info[i].ID]);
                                    // console.log(dict[animal + data[j].info[i].ID].bounds);
                                    // console.log(dict[animal + data[j].info[i].ID].bounds.width);
                                    // console.log("***********************************************");
                                    // dict[animal + data[j].info[i].ID].position = destination;
                                    dict[animal + data[j].info[i].ID].scale(scale);
                                    // dict[animal + data[j].info[i].ID].setPosition(destination);
                                    // console.log(dict[animal + data[j].info[i].ID]);
                                    dict[animal + data[j].info[i].ID].visible = true;

                                    // Fin Prueba David //
                                    
                                    id.push(data[j].info[i].ID);
                                    // console.log(animal + data[j].info[i].ID);
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
                                        x_relativa = data[j].info[i].Position[0]*(width/num_cols_repartir);
                                        y_relativa = data[j].info[i].Position[1]*(height/num_filas_repartir);
                                        destination = new Point(x_relativa,y_relativa);
                                        // // David
                                        // console.log(destination);
                                        // // Fin David
                                        vector = destination.subtract(dict[animal + data[j].info[i].ID].position);
                                        dict[animal + data[j].info[i].ID].position = dict[animal + data[j].info[i].ID].position.add(vector.divide(velocidad)); //vector.divide(velocidad)
 
                                    }
                                    // // Prueba David
                                    // if(i == data[j].info.length -1 && vector.length < 2 && j == data.length -1)
                                    // {
                                    //     console.log("he entrado y voy a desactivar el view.onFrame")
                                    //     view.onFrame = undefined;
                                    //     $('#inicio').trigger('click');
                                    // }
                                    // Fin Prueba David
                                }       
                            };
                        }//fin del else
                    }//fin del iniciar
                }//fin del if data > 0
                console.log("ha salido del if");
            }//fin del success
        })
    }
    // inicio_ajax.onclick = var_ajaxCall();

    Raster.prototype.rescale = function(width, height) {
        this.scale(width / this.width, height / this.height);
    };

    createOverlay();
    init();
}

function setTrainingMode()
{
    $(".overlay-play-button__overlay").css("visibility", "hidden");
    // $("#overlay").css(
    //     {"-webkit-transition":".4s ease-in-out opacity",
    //     "-moz-transition": ".4s ease-in-out opacity",
    //     "-o-transition": ".4s ease-in-out opacity",
    //     "transition": ".4s ease-in-out opacity"
    //     });
    $("#contenedor_canvas").hover(
        function(){
            $("#overlay").fadeIn();
        }, 
        function(){
            $("#overlay").fadeOut();
        }
    );
      
}

function createOverlay()
{
    var width = $("#myCanvas").width();
    var height = $("#myCanvas").height();
    var margin_left = parseInt($("#myCanvas").css("margin-left").replace("px",""));
    var margin_top = parseInt($("#myCanvas").css("margin-top"));
    var margin_bottom = parseInt($("#myCanvas").css("margin-bottom"));
    var border = parseInt($("#myCanvas").css("border-left-width").replace("px",""));

    $("#overlay").css("margin-left", margin_left+border);
    $("#overlay").css("margin-top", margin_top+border);
    $("#overlay").css("margin-bottom", margin_bottom);
    // $("#overlay").css("postion", "absolute");
    $("#overlay").css("z-index", 10);
    $("#overlay").width(width);
    $("#overlay").height(height);

    $(".overlay_under").width(width);
    $(".overlay_under").height(height);
    $(".overlay_under").css({"display": "flex", "align-items": "baseline"});

    
    $(".overlay-play-button__overlay").attr("onclick","setTrainingMode(); var_ajaxCall()");
    // $(".overlay-play-button__overlay").attr("onclick","setTrainingMode();");

    $("#opciones").css("margin-top", margin_top);
    $("#opciones").css("left", width+margin_left+2*border);
    $("#opciones").css("margin-left", "5%");

    $("#contendeor_canvas_opciones").height(height+margin_bottom+margin_top);
    $("#btn_siguiente").css("margin-left", margin_left+border);

}


var centesimas = 0;
var segundos = 0;
var minutos = 0;
var horas = 0;


function init() {
    let l, m, n, control
    // l = setInterval(change_value1, 500);
    // m = setInterval(change_value2, 500);
    // n = setInterval(change_value3, 500);
    l = setInterval(change_value("1"), 500);
    m = setInterval(change_value("2"), 500);
    n = setInterval(change_value("3"), 500);
    control = setInterval(cronometro,10);
}

function cronometro () {
    // if (centesimas < 99) {

    centesimas = parseInt(centesimas);
    segundos = parseInt(segundos);
    minutos = parseInt(minutos);
    horas = parseInt(horas);

    centesimas = (centesimas+1)%100;
    if (centesimas < 10) { centesimas = "0"+centesimas }
    // Centesimas.innerHTML = ":"+centesimas;
    // }
    // if (centesimas == 99) {
    //     centesimas = -1;
    // }
    if (centesimas == 0) {
        segundos = (segundos+1)%60;
        if (segundos < 10) { segundos = "0"+segundos }
        Segundos.innerHTML = ":"+segundos;
    }
    if ( (centesimas == 0)&&(segundos == 0) ) {
        minutos = (minutos +1)%60;
        if (minutos < 10) { minutos = "0"+minutos }
        Minutos.innerHTML = ":"+minutos;
    }
    if ( (centesimas == 0)&&(segundos == 0)&&(minutos == 0) ) {
        horas ++;
        if (horas < 10) { horas = "0"+horas }
        Horas.innerHTML = horas;
    }
}

function change_value(id)
{
    let input = parseInt(document.getElementById('input'+id).value);
    if (input >= 0 && input <= 4)
    {
        document.getElementById(id).innerHTML = (input+1)*5;
    }
    else
    {
        document.getElementById(id).innerHTML = 30;
    }
}

// function change_value1()
// {
//     // document.getElementById('p').innerHTML = document.getElementById('input').value
//     let input = parseInt(document.getElementById('input1').value);
//     if (input >= 0 && input <= 4)
//     {
//         document.getElementById("1").innerHTML = (input+1)*5;
//     }
//     else
//     {
//         document.getElementById("1").innerHTML = 30;
//     }

// }
// function change_value2()
// {
//     // document.getElementById('p').innerHTML = document.getElementById('input').value
//     let input = parseInt(document.getElementById('input2').value);
//     if (input >= 0 && input <= 4)
//     {
//         document.getElementById("2").innerHTML = (input+1)*5;
//     }
//     else
//     {
//         document.getElementById("2").innerHTML = 30;
//     }

// }
// function change_value3()
// {
//     // document.getElementById('p').innerHTML = document.getElementById('input').value
//     let input = parseInt(document.getElementById('input3').value);
//     if (input >= 0 && input <= 4)
//     {
//         document.getElementById("3").innerHTML = (input+1)*5;
//     }
//     else
//     {
//         document.getElementById("3").innerHTML = 30
//     }

// }
// input.oninput = function() {
//     output.innerHTML = values[this.value];
// };


