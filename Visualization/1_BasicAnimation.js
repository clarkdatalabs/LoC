
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

/*Read in our data:
	1. our topojson world definitions
	2. record counts that have been smoothed over a 5 year window
	3. a lookup table for country names (they weren't included in our topojson data) */
d3.queue()
	.defer(d3.json, "data/world.json")
	.defer(d3.csv, "data/location_by_year_smooth.csv")
	.defer(d3.csv, "data/countries.csv")
	.await(ready);
	
/*Once map and LoC data are loaded, do the following*/
function ready (error, data, LoC, countryLookup) {
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

	//extract country features and draw initial country shapes
	var countries = topojson.feature(data, data.objects.countries).features	
	countrySelection = map.selectAll(".country")
		.data(countries)
		.enter().append("path")
		.attr("class", "country")
		.attr("d", path)
		.attr("fill", null)
		.attr("fill", noDataColor)
		
	
	//updates the graphic periodically
	function updateDraw(elapsed){
	//draw countries
		year = startYear + ((1 + year  % startYear) % (endYear - startYear))
		//year = (Math.floor(elapsed/timeStep) % (endYear - startYear)) +startYear
		
		yearBox.textContent = year
		
			//change fill color to scale with count
			countrySelection.transition().attr("fill", function(d){
				if (LoCData[parseInt(d.id)] != undefined){
					if (LoCData[parseInt(d.id)][year] != undefined){
						return LoCData[parseInt(d.id)][year];
					} else {return noDataColor}
				} else {return noDataColor}
			})
			
	}
	
	//run updateDraw after every timeStep milliseconds
	d3.interval(updateDraw,timeStep);		
	}
	
