console.log("js has been called");

var margin = { top: 50, left: 50, right: 50, bottom: 50},
	height = 500 - margin.top - margin.bottom,
	width = 800 - margin.right - margin.left;

var svg = d3.select("#map")
	.append("svg")
	.attr("height", height + margin.top + margin.bottom)
	.attr("width", width + margin.right + margin.left)
	.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top +")");

/*Read in topojson*/
d3.queue()
	.defer(d3.json, "worldv1.json")
	.defer(d3.csv, "location_summary.csv")
	.await(ready);

/*Create a new projection using mercator (geoMercator)
and center it (translate)*/
var projection = d3.geoMercator()
	.translate([width /2, height / 2])	/*center in our visual*/
	.scale(110)
	
	
//create a path using (geoPath) using the projection
var path = d3.geoPath()
	.projection(projection)


	
/*Once map data is loaded, do the following*/
function ready (error, data, LoC) {
	var LoCData = [];
	LoC.forEach(function(d){
		LoCData[d.ISOnumeric3] = d;
	})
	console.log(data);
	console.log(LoCData);
	maxcount = 
	var countries = topojson.feature(data, data.objects.countries).features
	console.log(countries)
	
	svg.selectAll(".country")
		.data(countries)
		.enter().append("path")
		.attr("class", "country")
		.attr("count",function(d){
			if (LoCData[parseInt(d.id)] !== undefined){
				return LoCData[parseInt(d.id)].count;
			}
		})
		.attr("d", path)
		//add the class 'selected'
		.on('mouseover', function(d) {
			d3.select(this).classed("selected", true)
		})
		//remove the class 'selected'
		.on('mouseout', function(d) {
			d3.select(this).classed("selected", false)
		})
	
	console.log(LoC)
		
	}
	
