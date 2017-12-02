
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


/*Read in topojson*/
d3.queue()
	.defer(d3.json, "worldv1.json")
	.defer(d3.csv, "location_by_year.csv")
	.await(ready);
	
/*Once map and LoC data are loaded, do the following*/
function ready (error, data, LoC) {

	
	console.log("worldv1.json data:")
	console.log(data)
	
	console.log("location_by_year.csv:")
	console.log(LoC)
	
	//convert counts to integers
	LoC.forEach(function(d){
		d.count = +d.count;
	})
	
	//Define color scale function
	var maxCount = d3.max(LoC, function(d) { return d.count; });
	var baseColor = "#cccccc"
	var countryColor = d3.scalePow()
		.exponent(.15)
		.domain([0,maxCount])
		.range([baseColor, "red"])
		.clamp(true);
	
	
	//build LoCData array	
	var LoCData = {};
	LoC.forEach( function(d){
		if (LoCData[d.ISOnumeric3] == undefined){
			LoCData[d.ISOnumeric3] = {}
		}
		LoCData[d.ISOnumeric3][d.pubDate]= d.count
				}
	)
	

	//LOG LoCData
	console.log("LoCData:")
	console.log(LoCData);
	
	console.log(countryColor(LoCData[8][1999]))
	
	//extract country features
	var countries = topojson.feature(data, data.objects.countries).features	
	
	//Draw initial country shapes
//	svg.selectAll(".country")
//		.data(countries)
//		.enter().append("path")
//		.attr("class", "country")
//		.attr("d", path)
//		.attr("fill", null)
//		//.attr("fill", baseColor)
	
	
	//updates the graphic periodically
	function updateDraw(elapsed){
	//draw countries
		year = Math.floor(elapsed/1000)+1900
		
		console.log("year: " + year	)
		
		
		svg.selectAll("country")
			.data(countries)
			.enter().append("path")
			.attr("class", "country")
			.attr("d", path)
			
			//change fill color to scale with count
			.attr("fill", function(d){
				//return countryColor(d.id) 
				if (LoCData[parseInt(d.id)] != undefined){
					if (LoCData[parseInt(d.id)][year] != undefined){
						//console.log(LoCData[parseInt(d.id)][parseInt(year)])
						return countryColor(LoCData[parseInt(d.id)][year]);
					} else {return baseColor}
				} else {return baseColor}
			})
			
			//define .count attribute
/*			.attr("count",function(d){
				if (LoCData[parseInt(d.id)][year] !== undefined){
					return LoCData[parseInt(d.id)][year].count;
				} else {return 0}
			})*/
			
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
	}
	
	//d3.interval(updateDraw(Math.floor(elapsed/1000)+1800),1000);
	d3.interval(updateDraw,1000);
	
	console.log("data:")
	console.log(data);
		
		
	console.log(LoC)
		
	}
	
