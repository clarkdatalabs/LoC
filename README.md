
![cover photo](https://github.com/clarkdatalabs/LoC/blob/master/Visualization/images/LoC.jpg?raw=true)

# Mapping Library of Congress Records by Subject Location

> by Daniel Tanner

Last May, the US Library of Congress made the largest [release](https://www.si.umich.edu/news/library-congress-opened-its-catalogs-why-it-matters#gsc.tab=0) of digital records in its history – metadata for over 25 million books, maps and recordings. People immediately started making some pretty cool visualizations to explore [patterns in the data](http://sappingattention.blogspot.com/2017/05/a-brief-visual-history-of-marc.html), or demonstrate the [incredible size](https://medium.com/@thisismattmiller/library-of-congress-lists-57ddd177f1e2?loclr=blogsig) of the release. This page follows my process of building an animated D3 map visualization, from data cleaning to adding features. Each of the pages below covers one step in the process.

0. [Preparing the Data](https://clarkdatalabs.github.io/LoC/Visualization/0_PreparingData.html) - Parse massive xml record files, cache and geocode subject locations, aggregate for our visualization.
1. [Basic Animation](https://clarkdatalabs.github.io/LoC/Visualization/1_BasicAnimation.html) - Build a D3 map that animates changing numbers of records about each country over time.
2. [Add a Tooltip](https://clarkdatalabs.github.io/LoC/Visualization/2_TooltipSelection.html) - Add a tooltip to display country name on hovering. Select a country on click to show record counts for that country.

```python
re.findall(r'(?<!\d)\d{4}(?!\d)',date_string)
```
```python
.translate({ord(c): None for c in '[];:?,.'})
```

```xml
 <datafield tag="260" ind1=" " ind2=" ">
    <subfield code="a">New York city,</subfield>
    <subfield code="b">Dau publishing co.,</subfield>
    <subfield code="c">c1899.</subfield>
```


```js

.on('click', function(d){
			selectionID = null;
			var clickSelection = d3.select(this)
			clickSelection.classed("selected", function(d){
				if (clickSelection.classed("selected")){
					return false	//if already selected, unselect it
				} else {
					selectionID = parseInt(d.id);
					selectionName = country[parseInt(d.id)];
					d3.selectAll(".selected").classed("selected", false);	//clear previous selection
					clickSelection.moveToFront()	//bring selected country to front of draw order
					return true}
			});
```
