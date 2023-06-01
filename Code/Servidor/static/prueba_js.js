function crearModelo()
{
    var json_inputs = {};
    json_inputs["presa"] = {};
    json_inputs["depredador"] = {};

    $("input").each(function(iter, item) 
    {
        console.log(item.getAttribute("type"));
        if(item.getAttribute("type") != "number" && item.getAttribute("type") != "range")
        {
            return;
        }
        
        var id = item.getAttribute("json_name");

        if(!id){return;}

        var index_referencia_agente = id.lastIndexOf("_");


        console.log(id);

        if(id.includes("presa") || id.includes("depredador"))
        {
            var agente = id.split("_").pop();
            id = id.slice(0,index_referencia_agente);

            var valor = item.value;

            if(id == "energia"){valor = String(parseInt(item.value) * 5)}

            json_inputs[agente][id] = valor;
        }
        else
        {
            json_inputs[id] = item.value;
        }
        json_inputs["nombre"] = $("#nombre_proyecto").text().trim()
    })

    console.log(json_inputs);
    model_id_parameter=$("#modelo_id").attr("modelo_id");
    json_inputs["modelo_id"]=model_id_parameter;
    var request = $.ajax({

        type: 'POST',
        data: JSON.stringify(json_inputs),
        contentType: 'application/json;charset=UTF-8',
        url: "http://localhost:5000/crearModelo",

        success: function(data) 
        {
            console.log(data);
        }
    });
}


function toggleInputs(destination)
{
    $(".container_inputs_overall").css("visibility", "visible");
    $(".inputs_presas").css("visibility", "visible");
    $("#filtrosEspecie").css("visibility", "visible");
    $(".inputs_depredadores").css("visibility", "visible");

    if(destination == "especie")
    {
        $(".container_inputs_overall").fadeOut();
        $(".inputs_presas").fadeOut();
        
        $("#filtrosEspecie").fadeIn();
        $(".inputs_depredadores").fadeIn();
        
    }
    else
    {
        
        $("#filtrosEspecie").fadeOut();
        $(".inputs_depredadores").fadeOut();
        $(".inputs_presas").fadeOut();

        $(".container_inputs_overall").fadeIn();
    }
}

function toggleInputsAgentes(destination)
{
    if(destination == "depredadores")
    {
        $(".inputs_presas").fadeOut();
        $(".inputs_depredadores").fadeIn();
    }
    else
    {
        $(".inputs_depredadores").fadeOut();
        $(".inputs_presas").fadeIn();
    }
}

function cambiar_valor(id, valor)
{
    document.getElementsByClassName(id)[0].innerHTML = 5*(parseInt(valor));
}



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

    var my_width = $(document).width();
    var my_height = $(document).height();

    var rel_prop_width = my_width/1440;
    var rel_prop_height = my_height/800;

    // set CSS variable
    document.documentElement.style.setProperty(`--rel_prop_width`, `${rel_prop_width}`);
    document.documentElement.style.setProperty(`--rel_prop_height`, `${rel_prop_height}`);


    $(".apartado path").attr("fill", "#1B1C1E");
    $(".apartado_active path").attr("fill", "#2F8DAB");
    $(".overlay-play-button__overlay").attr("onclick","setTrainingMode(); var_ajaxCall()");

    $("#crearModelo").css({"position": "absolute", "right":"10%", "bottom":"2%"})
    $("#btn_grafica").css({"position": "absolute", "right":"30%", "bottom":"2%"})

    document.querySelectorAll("input").forEach(function(item) {
        item.addEventListener("keypress", function (evt) {
            evt.preventDefault();
        });
    });

    mi_canvas = $("#myCanvas");
    paper.setup('myCanvas');

    var id = [];
    var dict = {};
    var vector;
    var velocidad=0;
    var x_relativa;
    var y_relativa;

    var width = $("#myCanvas").width();
    var height = $("#myCanvas").height();
    
    // Seteamos el size que queremos para el canvas
    paper.view.viewSize = new Size(width,height);
    
    // Seteamos un offset para ver bien todos los agentes
    paper.view.translate(new Point(width/(num_cols_repartir*2),height/(num_filas_repartir*2)));

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
                        if(data[j].info[i].Sprite == "/assets/lobo.png"){
                            var animal = "lobo";
                        }else if(data[j].info[i].Sprite == "/assets/conejo.png"){
                            var animal = "conejo";
                        }else if(data[j].info[i].Sprite == "/assets/cesped.png"){
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
                                if(data[j].info[i].Sprite == "/assets/lobo.png"){
                                    var animal = "lobo";
                                }else if(data[j].info[i].Sprite == "/assets/conejo.png"){
                                    var animal = "conejo";
                                }else if(data[j].info[i].Sprite == "/assets/cesped.png"){
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

                                    if(data[j].info[i].Sprite == "/assets/lobo.png"){
                                        var animal = "lobo";
                                    }else if(data[j].info[i].Sprite == "/assets/conejo.png"){
                                        var animal = "conejo";
                                    }else if(data[j].info[i].Sprite == "/assets/cesped.png"){
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
                // setTimeout(function(){var_ajaxCall();}, 2000);
                console.log("ha salido del if");
            }//fin del success
        })
    }


    Raster.prototype.rescale = function(width, height) {
        this.scale(width / this.width, height / this.height);
    };

    // $(".overlay-play-button__overlay").attr("onclick","setTrainingMode(); var_ajaxCall()");

    chart = new Highcharts.Chart({
        // Definimos el estilo de grafica que será y de donde se cogen los datos
        chart: {
            renderTo: 'fig02',
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
    $(".overlay-play-button__overlay").fadeOut();
    const yourFunction = async () => {
        await delay(400);
        $(".overlay-play-button__overlay").css("visibility", "hidden");
    };
    
    $("#contenedor_canvas").hover(
        function(){
            $("#overlay").fadeIn();
        }, 
        function(){
            $("#overlay").fadeOut();
        }
    );
      
}
