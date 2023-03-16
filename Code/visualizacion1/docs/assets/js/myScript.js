

paper.install(window);
window.onload = function() {
    // bind paper to the canvas
    paper.setup('myCanvas');
    
    var width1 = 50,
        height1 = 50,
        x = [],
        y = [],
        x1 = [],
        y1 = [];

    let inicio_ajax = document.getElementById("inicio_ajax");
    console.log(inicio_ajax);
    inicio_ajax.onclick = ajaxCall;
    var actual = [];
    var anterior = [];

    /*function ajaxCall() {
        var request = $.ajax({
            type: 'GET',
            url: 'http://localhost:5000/prueba/1',
            success: function(data) {
                // console.log(data);
                // var info = {};
                try
                {    
                    anterior = actual;

                    actual = data;
                    
                    var new_numJSON = actual.length - anterior.length;

                    var difference = actual.slice(-new_numJSON);
                    for (var i=0;i<difference.length;i++){
                        x.push(difference[i].coord_x);
                        y.push(difference[i].coord_y);
                        x1.push(difference[i].coord_y);
                        y1.push(difference[i].coord_x);

                    }
                }
                catch(error)
                {
                    console.log("Todavía no hay nada");
                    actual = data;
                    console.log(actual);
                }

                console.log(data[data.length - 1]["Iteration"]);
                if(data[data.length - 1]["Iteration"] == 100)
                {
                    request.abort();
                    console.log(x);
                    console.log(y);
                }
                else
                {
                    setTimeout(function(){ajaxCall(); /send_data(difference)/}, 1000);
                }
            }
        });

    }*/
    var j,k,l;
    var lobos = [];
    var conejos = [];
    var contLobo=0;
    var contConejo=0;
    function ajaxCall() {
        var request = $.ajax({
            type: 'GET',
            url: 'http://localhost:5000/devolver',
            success: function(data) {

                console.log(data.length);
                for(var j=0;j<data.length;j++){

                    //HACER QUE DIFERENCIE ENTRE UN STEP Y EL SIGUIENTE PARA MOVER A OTRO SITIO
                    for(var i=0;i<data[j].info.length;i++){
                        if(data[j].info[i].Sprite == "lobo.png"){
                            console.log("entra lobo");
                            lobos.push(data[0].info[i]);
                            contLobo++;
                        }else if(data[j].info[i].Sprite == "conejo.png"){
                            console.log("entra conejo");
                            conejos.push(data[0].info[i]);
                            contConejo++;
                        }
                    }

                    console.log(lobos);
                    console.log(conejos);
                    crear(lobos,contLobo,conejos,contConejo);
                }
            }
        })
    }

    Raster.prototype.rescale = function(width, height) {
        this.scale(width / this.width, height / this.height);
    };
    
   
    function crear(dataL,contL,dataC,contC){
        for(var i = 0; i < contL; i++) {
            eval('var lobo' + dataL[i].id + '= new Raster({ source: "'+ dataL[i].Sprite +'", position: view.center});');
        }
        console.log("lobo");
        console.log(lobo4);
        for(var i = 0; i < contC; i++) {
            eval('var conejo' + dataC[i].id + '= new Raster({ source: "'+ dataC[i].Sprite +'", position: view.center});');
        }
        console.log("conejo");

        view.draw();

        var destination = new Point(x[0],y[0]);

        var destination1 = new Point(x1[0],y1[0]);
        
        let inicio = document.getElementById("inicio");
        let fin = document.getElementById("fin");
        var animating = false;
        inicio.onclick = iniciar; 
        fin.onclick = finalizar; 
        function iniciar(evento,) {
            animating = true;
            lobo4.visible = true;
            console.log(animating);
        }
        function finalizar(evento) {
            animating = false;
            console.log(animating);
            lobo4.visible = false;
            console.log(lobos);
        }
        
        view.onFrame = function(event){
            if(animating){
                //REVISAR QUE EL MOVIMIENTO QUE ESTÁ HACIENDO ES CORRECTO
                var vector
                var vector1
                for (var i =0;i < lobos.length;i++){
                    vector = destination.subtract(lobo4.position);
                    lobo4.position = lobo4.position.add(vector.divide(lobos.length*40));
                    lobo4.content = Math.round(vector.length);

                    vector1 = destination1.subtract(conejo1.position);
                    conejo1.position = conejo1.position.add(vector1.divide(conejos.length*40));
                    conejo2.content = Math.round(vector1.length);
                    
                    if (vector.length < lobos.length) {
                    
                        destination = new Point(lobos[i].Position[0],lobos[i].Position[1]);
                    }
                    if (vector1.length < conejos.length) {
                    
                        destination1 = new Point(conejos[i].Position[0],conejos[i].Position[1]);
                    }
                }
            }
        };

    }



   /*
    const prueba = d3.json("http://localhost:5000/prueba/2",
        function(data){
            for (var i =0;i < data.length;i++){
                x.push(data[i].coord_x)
                y.push(data[i].coord_y)
            }
            console.log(x)
            console.log(y)


           
            Raster.prototype.rescale = function(width, height) {
                this.scale(width / this.width, height / this.height);
            };
                
            var data_URL = "image.png";
            var data_URL_1 = "persona.png";

            var path = new Raster({
                source: data_URL,
                position: view.center
            });

            var path1 = new Raster({
                source: data_URL_1,
                position: view.center
            });

            view.draw();

            path.rescale(100,100);

            var destination = new Point(x[0],y[0]);

            var destination1 = new Point(x[1],y[1]);
            
            let inicio = document.getElementById("inicio");
            let fin = document.getElementById("fin");
            var animating = false;
            inicio.onclick = iniciar; 
            fin.onclick = finalizar; 
            function iniciar(evento) {
                animating = true;
                console.log(animating);
            }
            function finalizar(evento) {
                animating = false;
                console.log(animating);
            }
            
            view.onFrame = function(event){
                if(animating){
                    var vector
                    var vector1
                    for (var i =0;i < x.length;i++){
                        vector = destination.subtract(path.position);
                        path.position = path.position.add(vector.divide(x.length*40));
                        path.content = Math.round(vector.length);

                        vector1 = destination1.subtract(path1.position);
                        path1.position = path1.position.add(vector1.divide(x.length*40));
                        path1.content = Math.round(vector1.length);
                        
                        if (vector.length < x.length) {
                        
                            destination = new Point(x[i],y[i]);
                        }
                        if (vector1.length < x.length) {
                        
                            destination1 = new Point(x[i],y[i]);
                        }
                    }
                }
            };
            

        }
    )*/

    // view.draw();
}