

paper.install(window);
window.onload = function() {
    // bind paper to the canvas
    paper.setup('myCanvas');
    
    // var rectangle = new Rectangle(new Point(50, 50), new Point(150, 100));
    // var path = new Path.Rectangle(rectangle);
    // path.fillColor = '#e9e9ff';
    // path.strokeColor = 'black';
    // path.strokeWidth = 2;
    
    // path.selected = true;
    // path.closed = true;
    
    // var path = new Path.Circle({
        //     center: view.center,
        //     radius: 70,
        //     fillColor: 'red'
        //     });
    Raster.prototype.rescale = function(width, height) {
        this.scale(width / this.width, height / this.height);
    };
        
    var data_URL = "image.png";

    var path = new Raster({
        source: data_URL,
        position: view.center
    });

    view.draw();
    // var path = new Raster("image.png");

    path.rescale(100,100);

    // var destination = new Point.random()*view.size;
    // console.log(new Point(10,5));
    // console.log(new Point.random().multiply(view.size));
    // var x1 = Math.random();
    // var y1 = Math.random();

    // var destination = new Point(x1 * view.size._width, y1 * view.size._height);
    var destination = new Point.random().multiply(view.size);

    // console.log(view.size);
    // console.log(destination);
    // console.log(path.position);
    // console.log(destination.subtract(path.position));

    view.onFrame = function(event){
        var vector = destination.subtract(path.position);
        path.position = path.position.add(vector.divide(30));
        path.content = Math.round(vector.length);
        
        if (vector.length < 5) {
            destination = new Point.random().multiply(view.size);
        }
    };

    // view.draw();
}