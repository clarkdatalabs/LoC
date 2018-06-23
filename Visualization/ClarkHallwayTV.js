
//define basic visualization parameters
var startYear = 1900; //1400 is a good early start
	endYear = 2010;
	timeStep = 100;
	year = startYear;
	noDataColor = "#cccccc"
	maxColor = "red"
	minColor = "#8798b2"
	
//define map size based on screen		
var mapWidth = mapBox.clientWidth;
	mapHeight = mapBox.clientHeight;

//define global variable to track which country is selected
var selectionID = null;
var selectionName = null;

var map = d3.select("#map")
	.append("g")

	
/*Create a new projection using mercator (geoMercator)
and center it (translate)*/
var projection = d3.geoMercator()
	.translate([mapWidth/2, mapHeight/1.65])	/*center in our visual*/
	.scale(mapWidth/6.3)					/*initial scale factor for the geojson map I'm using*/

//create a path using (geoPath) using the projection
var path = d3.geoPath()
	.projection(projection)
	

	
//Define MoveToFront function
d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};


//		==TOOLTIP==

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
  

/*Read in our data:
	1. our topojson world definitions
	2. record counts that have been smoothed over a 5 year window
	3. a lookup table for country names (they weren't included in our topojson data) */
d3.queue()
	.defer(d3.json, "data/world.json")
	.defer(d3.csv, "data/location_by_year_smooth.csv")
	.defer(d3.csv, "data/countries.csv")
	.defer(d3.csv, "data/year_count.csv")
	.await(ready);
	
/*Once map and LoC data are loaded, do the following*/
function ready (error, data, LoC, countryLookup, yearCount) {
	//convert counts to integers
	LoC.forEach(function(d){
		d.smooth5 = +d.smooth5;
	})
	
	//Define color scale function
	var maxCount = d3.max(LoC, function(d) { return d.smooth5; });	
	var countryColor = d3.scalePow()
		.exponent(.2)
		.domain([0,maxCount])
		.range([minColor, maxColor])
		.clamp(true);
	
	//build LoCData data object	
	var LoCData = {};
	LoC.forEach( function(d){
					if (LoCData[d.ISOnumeric3] == undefined){
						LoCData[d.ISOnumeric3] = {}
					}
					LoCData[d.ISOnumeric3][parseInt(d.pubDate)]= {}
					LoCData[d.ISOnumeric3][parseInt(d.pubDate)]["color"] = countryColor(d.count)
					LoCData[d.ISOnumeric3][parseInt(d.pubDate)]["count"] = parseInt(d.count)
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
	
	//build year_count lookup table
	var year_count = {};
	yearCount.forEach( function(d){
		year_count[d.year] = d.recordCount
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
	console.log(country)
	console.log("yearCount:")
	console.log(yearCount);

	//extract country features and draw initial country shapes
	var countries = topojson.feature(data, data.objects.countries).features	
	countrySelection = map.selectAll(".country")
		.data(countries)
		.enter().append("path")
		.attr("class", "country")
		.attr("d", path)
		.attr("fill", null)
		.attr("fill", noDataColor)

	console.log("countrySelection: ")
	console.log(countries)
	
	//Function to select random country when the page is loaded:
	var randomCountryID = function (obj) {
		var keys = Object.keys(obj)
		return keys[ keys.length * Math.random() << 0];
	};
	
	
	//updates the graphic periodically
	function updateDraw(elapsed){
		
	//choose an new country whenever the timeline restarts
	if (year == startYear){
		selectionID = randomCountryID(country)
		d3.selectAll(".selected").classed("selected", false);	//clear previous selection
		countries.select("#selectionID")
			.classed("selected", true)
			.moveToFront();
		}
	
	year = (( (year  % startYear) + 1 ) % (endYear - startYear)) + startYear
	console.log("year:", year)
			
	yearBox.textContent = year
	
	//change header to display count of records of selected country
	if (selectionID == null){ //if nothing selected
		header.textContent = "Library of Congress book records with subject location metadata: " 
			+ parseInt(year_count[year])
				.toLocaleString();
		} else { 		//if country is selected
		if (LoCData[selectionID][year] != undefined){ 
			var selectionCount = LoCData[selectionID][year]["count"];
		}	else { var selectionCount = 0 }
		header.textContent = "Library of Congress book records about " 
			+ country[selectionID] + ": " 
			+ selectionCount.toLocaleString()
		}
			
		
		//change fill color to scale with count
		countrySelection.transition().attr("fill", function(d){
			//return countryColor(d.id) 
			if (LoCData[parseInt(d.id)] != undefined){
				if (LoCData[parseInt(d.id)][year] != undefined){
					//console.log(LoCData[parseInt(d.id)][parseInt(year)])
					return LoCData[parseInt(d.id)][year]["color"];
				} else {return noDataColor}
			} else {return noDataColor}
		})
			
	}
	
	

	//run updateDraw after every timeStep milliseconds
	d3.interval(updateDraw,timeStep);		
	}
	
