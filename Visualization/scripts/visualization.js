console.log("js has been called");

var margin = { top: 50, left: 50, right: 50, bottom: 50},
	height = 750 - margin.top - margin.bottom,
	width = 1200 - margin.right - margin.left;

var svg = d3.select("#map")
	.append("svg")
	.attr("height", height + margin.top + margin.bottom)
	.attr("width", width + margin.right + margin.left)
	.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top +")");

/*Create a new projection using mercator (geoMercator)
and center it (translate)*/
var projection = d3.geoMercator()
	.translate([width /2, height / 1.8])	/*center in our visual*/
	.scale(190)
	
//create a path using (geoPath) using the projection
var path = d3.geoPath()
	.projection(projection)

	//Define MoveToFront function
d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};

/*//Define the div for the tooltip
var div = d3.select("body").append("div")	
    .attr("class", "tooltip")				
    .style("opacity", 0);*/

/*Read in topojson*/
d3.queue()
	.defer(d3.json, "worldv1.json")
	.defer(d3.json, "world.json")
	.defer(d3.csv, "location_summary.csv")
	.await(ready);
	
/*Once map and LoC data are loaded, do the following*/
function ready (error, data, dataAlpha, LoC) {
	console.log("worldv1.json data")
	console.log(data)
	
	console.log("world.json data (with Alpha-2 codes)")
	console.log(dataAlpha)
	

	
	//convert counts to integers
	LoC.forEach(function(d){
		d.count = +d.count;
	})
	
	//Define color scale function
	var maxCount = d3.max(LoC, function(d) { return d.count; });
	var baseColor = "#cccccc"
	var countryColor = d3.scalePow()
		.exponent(.3)
		.domain([0,maxCount])
		.range([baseColor, "red"])
		.clamp(true);
		
	var LoCData = [];
	LoC.forEach(function(d){
		LoCData[d.ISOnumeric3] = d;
	})
	
	
	//LOG LoCData
	console.log("LoCData:")
	console.log(LoCData);
	
	var countries = topojson.feature(data, data.objects.countries).features
//	var countries = topojson.feature(data, data.objects.countries1).features
	
	console.log(countries)
	
	svg.selectAll(".country")
		.data(countries)
		.enter().append("path")
		.attr("class", "country")
		//define .count attribute
		.attr("count",function(d){
			if (LoCData[parseInt(d.id)] !== undefined){
				return LoCData[parseInt(d.id)].count;
			} else {return 0}
		})
		.attr("d", path)

		
		//change fill color to scale with count
		.attr("fill", function(d){
			if (LoCData[parseInt(d.id)] !== undefined){
				return countryColor(LoCData[parseInt(d.id)].count);
			} else {return baseColor}
		})
		
		//add the class 'selected'
		.on('mouseover', function(d) {
			d3.select(this)
				.classed("selected", true)
				.moveToFront()
		})
		//remove the class 'selected'
		.on('mouseout', function(d) {
			d3.select(this)
				.classed("selected", false)
		})
	
	console.log("data:")
	console.log(data);
		
		
	console.log(LoC)
		
	}
	
