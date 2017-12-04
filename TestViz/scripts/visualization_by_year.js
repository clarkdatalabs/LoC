
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
		.exponent(.2)
		.domain([0,maxCount])
		.range([baseColor, "green"])
		//.ticks(3)
		.clamp(true);
	
	//build LoCData data object	
	var LoCData = {};
	LoC.forEach( function(d){
					if (LoCData[d.ISOnumeric3] == undefined){
						LoCData[d.ISOnumeric3] = {}
					}
					LoCData[d.ISOnumeric3][d.pubDate]= countryColor(d.count)
					}
	)
	

	//LOG LoCData
	console.log("LoCData:")
	console.log(LoCData);
	
	
	//extract country features
	var countries = topojson.feature(data, data.objects.countries).features	
	
	
	//Draw initial country shapes
	countrySelection = svg.selectAll(".country")
		.data(countries)
		.enter().append("path")
		.attr("class", "country")
		.attr("d", path)
		.attr("fill", null)
		.attr("fill", baseColor)
		
		//add the class 'highlighted' on mouseover
		.on('mouseover', function(d) {
			d3.select(this)
				.classed("highlighted", true)
				.moveToFront()
			d3.selectAll(".selected")	//bring selected country to the front
				.moveToFront()
				
		})
		//remove the class 'highlighted'
		.on('mouseout', function(d) {
			d3.select(this)
				.classed("highlighted", false)
		})
		
		//add the class 'selected' on click
		.on('click', function(d){
			clickSelection = d3.select(this)
				clickSelection.classed("selected", function(d){
					if (clickSelection.classed("selected")){
						return false	//if already selected, unselect it
					} else {
						d3.selectAll(".selected").classed("selected", false);	//clear previous selection
						clickSelection.moveToFront()	//bring selected country to front of draw order
						return true}
				})
			//how do I access data attributes of clickSelection?
			console.log("clickSelection: " + clickSelection)
			
		})
	
		
	
	//updates the graphic periodically
	function updateDraw(elapsed){
	//draw countries
		year = (Math.floor(elapsed/timeStep) % 110) +1900
		
		console.log("year: " + year	)
				
			//change fill color to scale with count
			countrySelection.transition().attr("fill", function(d){
				//return countryColor(d.id) 
				if (LoCData[parseInt(d.id)] != undefined){
					if (LoCData[parseInt(d.id)][year] != undefined){
						//console.log(LoCData[parseInt(d.id)][parseInt(year)])
						return LoCData[parseInt(d.id)][year];
					} else {return baseColor}
				} else {return baseColor}
			})
			
	}
	

	//run updateDraw after every timeStep milliseconds
	var timeStep = 200
	d3.interval(updateDraw,timeStep);		
	}
	
