var width = 960, height = 500;
var projection = d3.geo.transverseMercator()
                       .center([2.5, -38.5])
                       .rotate([66, 0])
                       .scale((height * 56.5) / 33)
                       .translate([(width / 2), (height / 2)]);
var svg = d3.select("body")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
var path = d3.geo.path().projection(projection)

svg.append("path")
    .attr("d", path);
    

d3.json("argentina_indec.json", function(error, json) {
    svg.selectAll("text")
    .data(topojson.feature(json, json.objects.provincias).features)
    .enter()
    .append("path")
    .attr("d", path)
    .attr("class", "land")
    .on("mouseover", function(d, i){
      d3.select("this")  
      .attr("fill", "tomato")
    })
    
});

d3.select(self.frameElement).style("height", height + "px");

