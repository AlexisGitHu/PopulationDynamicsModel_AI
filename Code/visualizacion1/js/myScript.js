var var_ajaxCall = null;
var chart = null;
var num_cols_repartir = 10;
var num_filas_repartir = 10;
var step = 0;
var j = 0;

function add_data_graph(datos)
{
    var x_step = datos[0];
    var y_lobo = datos[1][0];
    var y_conejo = datos[1][1];
    
    
    y_lobo_teorico = datos[2][0];
    y_conejo_teorico = datos[2][1];

    point_lobo = [x_step, y_lobo];
    point_conejo = [x_step, y_conejo];
    point_lobo_teorico = [x_step, y_lobo_teorico];
    point_conejo_teorico = [x_step, y_conejo_teorico];
    
    chart.series[0].addPoint(point_lobo, true);
    chart.series[1].addPoint(point_conejo, true);
    chart.series[2].addPoint(point_lobo_teorico, true);
    chart.series[3].addPoint(point_conejo_teorico, true);
}

paper.install(window);
window.onload = function() {
    mi_canvas = $("#myCanvas");
    paper.setup('myCanvas');

    var id = [];
    var dict = {};
    var vector;
    var velocidad=0;
    var x_relativa;
    var y_relativa;

    var margin_left_deseado = $(window).width()/20;
    var margin_top_deseado = $(window).height()/11;
    var margin_bottom_deseado = $(window).height()/11;

    var height_deseado = $(window).height()*8/11;
    var width_deseado = height_deseado*3/2;
    
    $("#myCanvas").width(width_deseado);
    $("#myCanvas").height(height_deseado);

    // Seteamos el size que queremos para el canvas
    paper.view.viewSize = new Size(width_deseado,height_deseado);
    
    // Seteamos un offset para ver bien todos los agentes
    paper.view.translate(new Point(width_deseado/(num_cols_repartir*2),height_deseado/(num_filas_repartir*2)));
    

    $("#myCanvas").css("margin-left", margin_left_deseado);
    $("#myCanvas").css("margin-top", margin_top_deseado);
    $("#myCanvas").css("margin-bottom", margin_bottom_deseado);
    
    var width = $("#myCanvas").width();
    var height = $("#myCanvas").height();


    var_ajaxCall = function ajaxCall() {
        // console.log("hola");
        var request = $.ajax({
            type: 'GET',
            url: 'http://localhost:5000/paint_data',
            success: function(datos) {
                if(datos.length > 0){
                    // Datos para graficar
                    datos_grafica = datos[1];
                    add_data_graph(datos_grafica[0]);

                    // Datos para visualización
                    data = datos[0];
                    // console.log(data)
                    $("#inicio_ajax").css("visibility","hidden");
                    console.log("entra en el if");
                    console.log(data);
                    if(velocidad == 0){
                        velocidad = 10;
                    }
                    j = 0;
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
                            
                            destination = new Point(x_relativa,y_relativa);             
                            eval('var ' + animal + data[j].info[i].ID + '= new Raster({ source: "'+ data[j].info[i].Sprite +'", position: '+ destination +'});');
                            dict[animal + data[j].info[i].ID] = eval(animal + data[j].info[i].ID);

                            var scale = 1/5;
                            dict[animal + data[j].info[i].ID].scale(scale);
                            dict[animal + data[j].info[i].ID].visible = true;

                            id.push(data[j].info[i].ID);
                        }
                    }
                    // if(step == 0)
                    // {
                        let inicio = document.getElementById("btn_siguiente");
                        inicio.onclick = iniciar;
                    // }
                    // else
                    // {
                        // Podríamos hacer que se ejecute también desde el step 0
                        $('#btn_siguiente').trigger('click');
                    // }
                    
                    function iniciar(evento,) {
                        j++;
                        if (j >= data.length){var_ajaxCall()}
                        else{
                            step++;
                            console.log("step" + j);
                            $("#step").text("#"+String(step));
                            add_data_graph(datos_grafica[j]);
                            // add_data_graph(datos[1][j]);
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

                                    destination = new Point(x_relativa,y_relativa);

                                    eval('var ' + animal + data[j].info[i].ID + '= new Raster({ source: "'+ data[j].info[i].Sprite +'", position: ' + destination + '});');                                
                                    dict[animal + data[j].info[i].ID] = eval(animal + data[j].info[i].ID);

                                    var scale = 1/5;
                                    dict[animal + data[j].info[i].ID].scale(scale);
                                    dict[animal + data[j].info[i].ID].visible = true;

                                    id.push(data[j].info[i].ID);
                                }else{
                                    console.log(animal + data[j].info[i].ID + "" + data[j].info[i].Alive);
                                    if(data[j].info[i].Alive == "False"){
                                        console.log("muere" + animal + data[j].info[i].ID);
                                        dict[animal + data[j].info[i].ID].visible = false;
                                    }
                                }
                            }
                            
                            var destination;
                            console.log("prueba");
                            var vectores = Array(data[j].info.length-1).fill(0);
                            var vuelta = 0;
                            view.onFrame = function(event){
                                console.log("view");
                                
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
                                        vector = destination.subtract(dict[animal + data[j].info[i].ID].position);

                                        vectores[i] = vector.length;
                                        vector_max = Math.max(...vectores);
                                        // console.log(vector_max)
                                        // console.log(vuelta);
                                        
                                        dict[animal + data[j].info[i].ID].position = dict[animal + data[j].info[i].ID].position.add(vector.divide(velocidad)); //vector.divide(velocidad) 
                                        
                                        if(vuelta != 0 && vector_max < 0.01)
                                        {
                                            console.log("")
                                            view.onFrame = null;
                                            console.log("YA");
                                            $('#btn_siguiente').trigger('click');
                                            break;
                                        }
                                    }
                                }       
                                vuelta++;
                            };
                            // $('#btn_siguiente').trigger('click');
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

    createOverlay();
    init();

    chart = new Highcharts.Chart({
        // Definimos el estilo de grafica que será y de donde se cogen los datos
        chart: {
            renderTo: 'fig02',
            // events: {
            //     load: requestData,
            // },
            type: "line",
            animation: false,
            zoomType: 'x',
            panning: {
                enabled: true
            },
            panKey: 'shift',
        },
        // Configuramos los plotOtions para mostrar checkboxes en la leyenda
        plotOptions: {
            series: {
                showCheckbox: true,
                selected: true,
                events: {
                    checkboxClick: function () {
                        this.setVisible(!this.visible);
                    },
                },
                // showInNavigator: true,
            }
        },
        // Definimos el titulo del gráfico
        title: {
            text: 'Live data'
        },
        // Definimos el estilo del eje x
        xAxis: {
            type: 'linear',
            allowDecimals: false,
            min: 0
        },
        // Definimos el estilo del eje y
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Value',
                margin: 80
            }
        },
        // Definimos cómo queremos la leyenda
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            itemStyle: {
                fontSize:'17px',
                // font: '20pt Trebuchet MS, Verdana, sans-serif',
                color: '#000'
            },
        },
        // Definimos que queremos un ToolTip para ver los distintos valores que toman las graficas en cierto punto
        tooltip: {
            crosshairs: [true, true],
            shared: true
        },
        // Definimos las series distintas que vamos a tener
        series: [
        {
            name: '# lobos',
            data: []
        },
        {
            name: '# conejos',
            data: []
        },
        {
            name: '# lobos teoricos',
            data: []
        },
        {
            name: '# conejos teoricos',
            data: []
        }]
    });
}

function setTrainingMode()
{
    $(".overlay-play-button__overlay").css("visibility", "hidden");
    
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
    // $("#btn_siguiente").css("margin-left", margin_left+border);
    $("#btn_grafica").css("margin-left", margin_left+border);

}


var centesimas = 0;
var segundos = 0;
var minutos = 0;
var horas = 0;


function init() {

    for(let i = 1; i < 4; i++)
    {
        var input = document.getElementById("input"+String(i));
        var valor_actual = input.value;
        cambiar_valor(i, valor_actual);
    }
    
    control = setInterval(cronometro,10);
}

function cronometro () {
    centesimas = parseInt(centesimas);
    segundos = parseInt(segundos);
    minutos = parseInt(minutos);
    horas = parseInt(horas);

    centesimas = (centesimas+1)%100;
    if (centesimas < 10) { centesimas = "0"+centesimas }

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

function cambiar_valor(id, valor)
{
    document.getElementById(id).innerHTML = 5*(1+parseInt(valor));
}
