google.load("elements", "1", {packages : ["newsshow"]});
  
function onLoad()
{
	// Set the queries to USC Football and NHL
	var options = {
		"queryList" : [
		{
	  		"title" : "",
	  		"q" : ""
		}]
	}
	
	// get the keyword from parameter
	text_ = getURLParam("key")
	
	
	options.queryList[0].title = text_;
	options.queryList[0].q = text_;
	
	var content = document.getElementById('div_google');
	var newsShow = new google.elements.NewsShow(content, options);
	loadTimeline(text_);
}
  
<!--google.setOnLoadCallback(onLoad);-->

function getURLParam(strParamName)
{
	var strReturn = "";
	var strHref = window.location.href;
  	
	if ( strHref.indexOf("?") > -1 ) {
    	var strQueryString = strHref.substr(strHref.indexOf("?")).toLowerCase();
    	var aQueryString = strQueryString.split("&");
	    for ( var iParam = 0; iParam < aQueryString.length; iParam++ ) {
	    	if (aQueryString[iParam].indexOf(strParamName.toLowerCase() + "=") > -1 ) {
	        	var aParam = aQueryString[iParam].split("=");
	        	strReturn = aParam[1];
	        	break;
	    	}
    	}
	}
	
	return unescape(strReturn);
}

function load_twit()
{
	var keyword = getURLParam("key")
	
	new TWTR.Widget({
		version: 2,
		type: 'search',
		search: keyword,
		interval: 6000,
		title: keyword,
		subject: '',
		width: 295,
		height: 523,
		theme: {
		  shell: {
		    background: '#1b4457',
		    color: '#ffffff'
		  },
		  tweets: {
		    background: '#ffffff',
		    color: '#444444',
		    links: '#387c9c'
		  }
		},
		features: {
		  scrollbar: true,
		  loop: true,
		  live: true,
		  hashtags: true,
		  timestamp: true,
		  avatars: true,
		  toptweets: true,
		  behavior: 'default'
		}
	}).render().start();	
}


function loadTimeline(key){
			url = '/getTimeline?key="' + key + '"';
			$.ajax({
				type : "GET",
				dataType : "json",
				url : url,
				success : function(data) {
					displayTimeline(eval(data));
				}
			});
}


function displayTimeline(timeline){
console.log(timeline);
timeline=timeline;
days=timeline.days;
for (i=0;i < days.length ;i++){
console.log(timeline.days[i]);
}
return timeline;
}














