
![cover photo](https://github.com/clarkdatalabs/LoC/blob/master/Visualization/images/LoC.jpg?raw=true)

# Mapping Library of Congress Records by Subject Location

> by Daniel Tanner

In May 2017, the US Library of Congress made the largest [release](https://www.si.umich.edu/news/library-congress-opened-its-catalogs-why-it-matters#gsc.tab=0) of digital records in its history – metadata for over 25 million books, maps and recordings. People immediately started making some pretty cool visualizations to explore [patterns in the data](http://sappingattention.blogspot.com/2017/05/a-brief-visual-history-of-marc.html), or demonstrate the [incredible size](https://medium.com/@thisismattmiller/library-of-congress-lists-57ddd177f1e2?loclr=blogsig) of the release. This page follows my process of building an animated D3 map visualization, from data cleaning to adding features. Each of the pages below covers one step in the process.

0. [Preparing the Data](https://clarkdatalabs.github.io/LoC/Visualization/0_PreparingData.html) - Parse massive xml record files, cache and geocode subject locations, aggregate for our visualization.
1. [Basic Animation](https://clarkdatalabs.github.io/LoC/Visualization/1_BasicAnimation.html) - Build a D3 map that animates changing numbers of records about each country over time.
2. [Add a Tooltip](https://clarkdatalabs.github.io/LoC/Visualization/2_TooltipSelection.html) - Add a tooltip to display country name on hovering. Select a country on click to show record counts for that country.
