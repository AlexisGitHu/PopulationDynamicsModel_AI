

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
    var vector;
    var velocidad;
    let cambiar_velocidad = document.getElementById("cambiar_velocidad");
    cambiar_velocidad.onclick = cambiar;
    function cambiar(evento,) {
        velocidad = document.getElementById("velocidad").value;
    };
    function ajaxCall() {
        var request = $.ajax({
            type: 'GET',
            url: 'http://localhost:5000/visualizar',
            success: function(data) {
                console.log(velocidad);
                var j = 0;
                for(var i=0;i<data[j].info.length;i++){
                    if(data[j].info[i].Sprite == "lobo.png"){
                        var animal = "lobo";
                    }else if(data[j].info[i].Sprite == "conejo.png"){
                        var animal = "conejo";
                    }else if(data[j].info[i].Sprite == "hierva.png"){
                        var animal = "hierva";
                    }
                    if(!id.includes(data[j].info[i].ID)){
                        destination = new Point(data[j].info[i].Position[0],data[j].info[i].Position[1]);
                        eval('var ' + animal + data[j].info[i].ID + '= new Raster({ source: "'+ data[j].info[i].Sprite +'", position: view.center});');                                
                        dict[animal + data[j].info[i].ID] = eval(animal + data[j].info[i].ID);
                        id.push(data[j].info[i].ID);
                        console.log(animal + data[j].info[i].ID);
                    }
                }
                let inicio = document.getElementById("inicio");
                inicio.onclick = iniciar;
                function iniciar(evento,) {
                    j++;
                    console.log("step" + j);
                    for(var i=0;i<data[j].info.length;i++){
                        if(data[j].info[i].Sprite == "lobo.png"){
                            var animal = "lobo";
                        }else if(data[j].info[i].Sprite == "conejo.png"){
                            var animal = "conejo";
                        }else if(data[j].info[i].Sprite == "hierva.png"){
                            var animal = "hierva";
                        }
                        if(!id.includes(data[j].info[i].ID)){
                            destination = new Point(data[j].info[i].Position[0],data[j].info[i].Position[1]);
                            eval('var ' + animal + data[j].info[i].ID + '= new Raster({ source: "'+ data[j].info[i].Sprite +'", position: view.center});');                                
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
                            if(data[j].info[i].Sprite == "lobo.png"){
                                var animal = "lobo";
                            }else if(data[j].info[i].Sprite == "conejo.png"){
                                var animal = "conejo";
                            }else if(data[j].info[i].Sprite == "hierva.png"){
                                var animal = "hierva";
                            }
                            
                            if(id.includes(data[j].info[i].ID)){ 
                                destination = new Point(data[j].info[i].Position[0],data[j].info[i].Position[1]);
                                //eval(''+animal + data[j].info[i].ID+'')[0].position = destination;
                                vector = destination.subtract(dict[animal + data[j].info[i].ID].position);
                                dict[animal + data[j].info[i].ID].position = dict[animal + data[j].info[i].ID].position.add(vector.normalize()); //vector.divide(velocidad)
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
                                
                            
                            

                           
                           //console.log("acaba un info");
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
                        
                        
                        
                    //};
                }
            }
        })
    }

    Raster.prototype.rescale = function(width, height) {
        this.scale(width / this.width, height / this.height);
    };

   
}