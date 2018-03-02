

var startYear = 1400;
	endYear = 2010;
	timeStep = 100;
	year = startYear;


var mapWidth = mapBox.clientWidth;
	mapHeight = mapBox.clientHeight;
	histWidth = histBox.clientWidth;
	histHeight = histBox.clientHeight;

console.log("width", mapWidth)
console.log("height", mapHeight)



var map = d3.select("#map")
	.append("g")



/*Create a new projection using mercator (geoMercator)
and center it (translate)*/
var projection = d3.geoMercator()
	.translate([mapWidth/2, mapHeight/1.8])	/*center in our visual*/
	.scale(mapWidth/6.3)					/*initial scale factor for the geojson map we're using*/

//create a path using (geoPath) using the projection
var path = d3.geoPath()
	.projection(projection)
	
	
//Define MoveToFront function
d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};



//Prep the tooltip bits, initial display is hidden (copied from http://bl.ocks.org/mstanaland/6100713)
var tooltip = d3.select("#map")
	.append("g")
	.attr("class", "tooltip")
	.style("display", "none");
    
tooltip.append("rect")
  .attr("height", 20)
  .attr("fill", "white")
  .style("opacity", 0.5);

tooltip.append("text")
  .attr("x", 5)
  .attr("dy", "1.2em")
  .style("text-anchor", "left")
  .attr("font-size", "12px")
  .attr("font-weight", "bold");

/*Read in topojson*/
d3.queue()
	.defer(d3.json, "../world.json")
	.defer(d3.csv, "../data/location_by_year_smooth.csv")
	.defer(d3.csv, "../data/countries.csv")
	//.defer(d3.csv, "Visualization/location_by_year.csv")
	.await(ready);
	
/*Once map and LoC data are loaded, do the following*/
function ready (error, data, LoC, countryLookup) {
	//convert counts to integers
	LoC.forEach(function(d){
		d.smooth5 = +d.smooth5;
	})
	
	//Define color scale function
	var maxCount = d3.max(LoC, function(d) { return d.smooth5; });	
	//console.log("maxCount: ", maxCount)
	var baseColor = "#cccccc"
	var countryColor = d3.scalePow()
		.exponent(.2)
		.domain([0,maxCount])
		.range(["#8798b2", "red"])
		.clamp(true);
	
	//build LoCData data object	
	var LoCData = {};
	LoC.forEach( function(d){
					if (LoCData[d.ISOnumeric3] == undefined){
						LoCData[d.ISOnumeric3] = {}
					}
					LoCData[d.ISOnumeric3][parseInt(d.pubDate)]= countryColor(d.count)
		}
	)

	//build country lookup table
	var country = {};
	countryLookup.forEach( function(d){
		if (LoCData[d.ISOnumeric3] == undefined){
			LoCData[d.ISOnumeric3] = {}
		}
		country[d.ISOnumeric3] = d.countryName
		}
	)

	


	//LOG DATA TO CONSOLE
	console.log("world.json data:")
	console.log(data)
	console.log("LoC:")
	console.log(LoC)
	console.log("LoCData:")
	console.log(LoCData)
	console.log("country:")
	console.log(country);
	


	//extract country features and draw initial country shapes
	var countries = topojson.feature(data, data.objects.countries).features	
	countrySelection = map.selectAll(".country")
		.data(countries)
		.enter().append("path")
		.attr("class", "country")
		.attr("d", path)
		.attr("fill", null)
		.attr("fill", baseColor)
		
		//TOOLTIP
		//add the class 'highlighted' on mouseover
		.on('mouseover', function(d) {
			d3.select(this)
				.classed("highlighted", true)
				.moveToFront();
			d3.selectAll(".selected")	//bring selected country to the front
				.moveToFront();
			tooltip
				.style("display", null) //let default display style show
				.moveToFront()
				.select("text").text(country[parseInt(d.id)]);
			var dim = tooltip.select("text").node().getBBox();
			tooltip.select("rect").attr("width", dim.width+10);
		})
		//remove the class 'highlighted' on mouseout
		.on('mouseout', function(d) {
			d3.select(this)
				.classed("highlighted", false);
			tooltip.style("display", "none"); //hide tooltip on mousout
		})
		//move tooltip to follow mouse
		.on('mousemove', function(d) {
			var xPosition = d3.mouse(this)[0] + 10;
			var yPosition = d3.mouse(this)[1] - 25;
			tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");

		})
		
		//add the class 'selected' on click
		.on('click', function(d){
			console.log(country[parseInt(d.id)]);
			var selectionName = "Global"
			var clickSelection = d3.select(this)
			clickSelection.classed("selected", function(d){
				if (clickSelection.classed("selected")){
					return false	//if already selected, unselect it
				} else {
					selectionName = country[parseInt(d.id)];
					d3.selectAll(".selected").classed("selected", false);	//clear previous selection
					clickSelection.moveToFront()	//bring selected country to front of draw order
					return true}
			});
			console.log("clicky message:", selectionName)
			tooltip.moveToFront();
			countryName.textContent = selectionName;
		})
		
	
	//updates the graphic periodically
	function updateDraw(elapsed){
	//draw countries
		year = (( (year  % startYear) + 1 ) % (endYear - startYear)) + startYear
		console.log("year:", year)
		//year = (Math.floor(elapsed/timeStep) % (endYear - startYear)) +startYear
		
		yearBox.textContent = year
		
				
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
	d3.interval(updateDraw,timeStep);		
	}
	
