

paper.install(window);
window.onload = function() {
    // bind paper to the canvas
    paper.setup('myCanvas');
    
    var width1 = 50,
        height1 = 50,
        x = [12,234,234,12,3,4,2,21,34,4,1,312,54,23,2,1],
        y = [354,645,34,67,563,423,7,6545,63,47,56,34,456,234,67,233],
        x1 = [354,645,34,67,563,423,7,6545,63,47,56,34,456,234,67,233],
        y1 = [12,234,234,12,3,4,2,21,34,4,1,312,54,23,2,1];

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
    var id = [];
    var lista = [];
    var dict = {};
    var vector
    function ajaxCall() {
        var request = $.ajax({
            type: 'GET',
            url: 'http://localhost:5000/visualizar',
            success: function(data) {
                var j = 0;
                for(var i=0;i<data[j].info.length;i++){
                    console.log(data[j].info[i].ID);
                    if(data[j].info[i].Sprite == "lobo.png"){
                        var animal = "lobo";
                    }else if(data[j].info[i].Sprite == "conejo.png"){
                        var animal = "conejo";
                    }
                    if(!id.includes(data[j].info[i].ID)){
                        console.log("crea animal nuevo");
                        destination = new Point(data[j].info[i].Position[0],data[j].info[i].Position[1]);
                        eval('var ' + animal + data[j].info[i].ID + '= new Raster({ source: "'+ data[j].info[i].Sprite +'", position: view.center});');                                
                        dict[animal + data[j].info[i].ID] = eval(animal + data[j].info[i].ID);
                        id.push(data[j].info[i].ID);
                    }
                }
                console.log(dict);
                let inicio = document.getElementById("inicio");
                inicio.onclick = iniciar;
                function iniciar(evento,) {
                    j++;
                    console.log("iniciar" + j);

                    for(var i=0;i<data[j].info.length;i++){
                        console.log(data[j].info[i].ID);
                        if(data[j].info[i].Sprite == "lobo.png"){
                            var animal = "lobo";
                        }else if(data[j].info[i].Sprite == "conejo.png"){
                            var animal = "conejo";
                        }
                        if(!id.includes(data[j].info[i].ID)){
                            console.log("crea animal nuevo");
                            destination = new Point(data[j].info[i].Position[0],data[j].info[i].Position[1]);
                            eval('var ' + animal + data[j].info[i].ID + '= new Raster({ source: "'+ data[j].info[i].Sprite +'", position: view.center});');                                
                            dict[animal + data[j].info[i].ID] = eval(animal + data[j].info[i].ID);
                            id.push(data[j].info[i].ID);
                        }
                    }
                    var destination;
                    
                    /*
                    for(var i=0;i<data[j].info.length;i++){
                        console.log(data[j].info[i].ID);
                        if(data[j].info[i].Sprite == "lobo.png"){
                            var animal = "lobo";
                        }else if(data[j].info[i].Sprite == "conejo.png"){
                            var animal = "conejo";
                        }
                        if(!id.includes(data[j].info[i].ID)){
                            console.log("crea animal nuevo");
                            destination = new Point(data[j].info[i].Position[0],data[j].info[i].Position[1]);
                            eval('var ' + animal + data[j].info[i].ID + '= [new Raster({ source: "'+ data[j].info[i].Sprite +'", position: view.center}),'+destination+'];');                                
                            prueba = 7;
                            id.push(data[j].info[i].ID);
                        }
                    }*/
                    view.onFrame = function(event){
                        //for(var j=0;j<=5;j++){
                        
                        for(var i=0;i<data[j].info.length;i++){
                            console.log(data[j].info[i].ID);
                            if(data[j].info[i].Sprite == "lobo.png"){
                                var animal = "lobo";
                            }else if(data[j].info[i].Sprite == "conejo.png"){
                                var animal = "conejo";
                            }
                            
                            if(id.includes(data[j].info[i].ID)){ 
                                destination = new Point(data[j].info[i].Position[0],data[j].info[i].Position[1]);
                                console.log("mueve posicion");
                                //eval(''+animal + data[j].info[i].ID+'')[0].position = destination;
                                vector = destination.subtract(dict[animal + data[j].info[i].ID].position);
                                dict[animal + data[j].info[i].ID].position = dict[animal + data[j].info[i].ID].position.add(vector.divide(5*40));
                                dict[animal + data[j].info[i].ID].content = Math.round(vector.length);
                                
                                /*eval(animal + data[j].info[i].ID)[1] = destination;
                                console.log("ya existe");
                                vector = eval(animal + data[j].info[i].ID)[1].subtract(eval(animal + data[j].info[i].ID)[0].position);
                                eval(animal + data[j].info[i].ID)[0].position = eval(animal + data[j].info[i].ID)[0].position.add(vector.divide(5*40));
                                eval(animal + data[j].info[i].ID)[0].content = Math.round(vector.length);*/
                                /*if(data[j].info[i].Sprite == "lobo.png"){
                                    var destination = new Point(data[j].info[i].Position[0],data[j].info[i].Position[1]);
                                    eval('lobo' + data[j].info[i].ID)[1] = destination;
                                    console.log("ya existe");
                                    vector = eval('lobo' + data[j].info[i].ID)[1].subtract(eval('lobo' + data[j].info[i].ID)[0].position);
                                    eval('lobo' + data[j].info[i].ID)[0].position = eval('lobo' + data[j].info[i].ID)[0].position.add(vector.divide(5*40));
                                    eval('lobo' + data[j].info[i].ID)[0].content = Math.round(vector.length);
                                    //vector = destination.subtract(eval('lobo' + data[j].info[i].ID).position);
                                    //eval('lobo' + data[j].info[i].ID).position = eval('lobo' + data[j].info[i].ID).position.add(vector.divide(data[j].info.length*40));
                                } else if(data[j].info[i].Sprite == "conejo.png"){
                                    var destination = new Point(data[j].info[i].Position[0],data[j].info[i].Position[1]);
                                    eval('conejo' + data[j].info[i].ID)[1] = destination;
                                    console.log("ya existe");
                                    //vector = destination.subtract(eval('conejo' + data[j].info[i].ID).position);
                                    //eval('conejo' + data[j].info[i].ID).position = eval('conejo' + data[j].info[i].ID).position.add(vector.divide(data[j].info.length*40));
                                    //eval('conejo' + data[j].info[i].ID).content = Math.round(vector.length);
                                }*/  
                            }/*else{
                                console.log("crea animal nuevo");
                                destination = new Point(data[j].info[i].Position[0],data[j].info[i].Position[1]);
                                eval('var ' + animal + data[j].info[i].ID + '= [new Raster({ source: "'+ data[j].info[i].Sprite +'", position: view.center}),'+destination+'];');                                
                                prueba = 7;*/
                                //eval('var '+ String(animal + data[j].info[i].ID) + '=3;' );
                                //var temp = (eval(''+animal + data[j].info[i].ID+''))[1];
                                //console.log(temp.subtract(4));
                                //vector = destination.subtract((eval(''+animal + data[j].info[i].ID+''))[0].position);
                                //vector = (eval(''+animal + data[j].info[i].ID+''))[1].subtract((eval(''+animal + data[j].info[i].ID+''))[0].position);
                                //eval(animal + data[j].info[i].ID)[0].position = eval(animal + data[j].info[i].ID)[0].position.add(vector.divide(5*40));
                                //eval(animal + data[j].info[i].ID)[0].content = Math.round(vector.length);
                                /*if(data[j].info[i].Sprite == "lobo.png"){
                                    var destination = new Point(data[j].info[i].Position[0],data[j].info[i].Position[1]);
                                    eval('var lobo' + data[j].info[i].ID + '= [new Raster({ source: "'+ data[j].info[i].Sprite +'", position: view.center}),'+destination+'];');                                
                                    console.log("prueba");
                                    console.log(lobo0[1]);
                                    vector = eval('lobo' + data[j].info[i].ID)[1].subtract(eval('lobo' + data[j].info[i].ID)[0].position);
                                    eval('lobo' + data[j].info[i].ID)[0].position = eval('lobo' + data[j].info[i].ID)[0].position.add(vector.divide(5*40));
                                    eval('lobo' + data[j].info[i].ID)[0].content = Math.round(vector.length);
                                    //vector = destination.subtract(eval('lobo' + data[j].info[i].ID).position);
                                    //eval('lobo' + data[j].info[i].ID).position = eval('lobo' + data[j].info[i].ID).position.add(vector.divide(data[j].info.length*40));
                                    //eval('lobo' + data[j].info[i].ID).content = Math.round(vector.length);
                                }else if(data[j].info[i].Sprite == "conejo.png"){
                                    var destination = new Point(data[j].info[i].Position[0],data[j].info[i].Position[1]);
                                    eval('var conejo' + data[j].info[i].ID + '= [new Raster({ source: "'+ data[j].info[i].Sprite +'", position: view.center}),'+destination+'];');
                                    
                                    console.log(destination);
                                    //vector = destination.subtract(eval('conejo' + data[j].info[i].ID).position);
                                    //eval('conejo' + data[j].info[i].ID).position = eval('conejo' + data[j].info[i].ID).position.add(vector.divide(data[j].info.length*40));
                                    //eval('conejo' + data[j].info[i].ID).content = Math.round(vector.length);
                                }*/
                                
                            
                            

                           
                           console.log("acaba un info");
                           /*view.onFrame = function(event){
                                for(var i=0;i<id.length;i++){
                                    
                                    if(id[i] % 2 == 0){
                                        console.log(id[i]);
                                        vector = eval('lobo' + id[i])[1].subtract(eval('lobo' + id[i])[0].position);
                                        eval('lobo' + id[i])[0].position = eval('lobo' + id[i])[0].position.add(vector.divide(5*40));
                                        eval('lobo' + id[i])[0].content = Math.round(vector.length);
                                    }
                                    if(id[i] % 2 != 0){
                                        console.log(id[i]);
                                        vector = eval('conejo' + id[i])[1].subtract(eval('conejo' + id[i])[0].position);
                                        eval('conejo' + id[i])[0].position = eval('conejo' + id[i])[0].position.add(vector.divide(5*40));
                                        eval('conejo' + id[i])[0].content = Math.round(vector.length);
                                    }
                                }

                                //view.onFrame = null;
    */
                        }
                            
                    };
                           
                    //}
                        console.log(id);
                        /*
                            var vector
                            var vector1
                            for (var i =0;i < longitud;i++){
                                vector = destination.subtract(lobo0.position);
                                lobo0.position = lobo0.position.add(vector.divide(longitud*40));
                                lobo0.content = Math.round(vector.length);

                                vector1 = destination1.subtract(conejo1.position);
                                conejo1.position = conejo1.position.add(vector1.divide(longitud*40));
                                conejo1.content = Math.round(vector1.length);
                                
                                if (vector.length < lobos.length) {
                                    
                                    destination = new Point(x[i],y[i]);
                                }
                                if (vector1.length < conejos.length) {
                                
                                    destination1 = new Point(x1[i],y1[i]);
                                }
                            }*/
                        
                        
                        /*
                        for(var i =0;i<data[0].info.length;i++){
                            if(data[0].info[i].Sprite == "lobo.png"){
                                eval('var lobo' + data[0].info[i].ID + '= new Raster({ source: "'+ data[0].info[i].Sprite +'", position: view.center});');
                            }else if(data[0].info[i].Sprite == "conejo.png"){
                                eval('var conejo' + data[0].info[i].ID + '= new Raster({ source: "'+ data[0].info[i].Sprite +'", position: view.center});');
                            }
                        }
                        console.log(data[0].info[0].Position[0]);
                        visualizar(lobo0,conejo1,lobo2,data.length);
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
                        }*/
                    //};
                }
            }
        })
    }

    Raster.prototype.rescale = function(width, height) {
        this.scale(width / this.width, height / this.height);
    };
    function visualizar(lobo0,conejo1,lobo2,longitud){
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
            console.log(animating);
        }
        function finalizar(evento) {
            animating = false;
            console.log(animating);
        }
        
        view.onFrame = function(event){
            if(animating){
                //REVISAR QUE EL MOVIMIENTO QUE ESTÁ HACIENDO ES CORRECTO
                var vector
                var vector1
                for (var i =0;i < longitud;i++){
                    vector = destination.subtract(lobo0.position);
                    lobo0.position = lobo0.position.add(vector.divide(longitud*40));
                    lobo0.content = Math.round(vector.length);

                    vector1 = destination1.subtract(conejo1.position);
                    conejo1.position = conejo1.position.add(vector1.divide(longitud*40));
                    conejo1.content = Math.round(vector1.length);
                    
                    if (vector.length < lobos.length) {
                        
                        destination = new Point(x[i],y[i]);
                    }
                    if (vector1.length < conejos.length) {
                    
                        destination1 = new Point(x1[i],y1[i]);
                    }
                }
            }
        };
    }

   /*
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

*/

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