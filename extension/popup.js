var last_url = ""
var cur_url = ""
var temp = ""

chrome.webRequest.onBeforeRequest.addListener(
	function(details)
	{
		var type = details.type
		var done = 0;

		if(type == "main_frame")
		{	
			cur_url = details.url
			cur_url = cur_url.substring(cur_url.lastIndexOf("://")+3, cur_url.length);
			cur_url = cur_url.substring(0, cur_url.indexOf("/"));
			
			
			if(cur_url != last_url && cur_url.indexOf("google") == -1)
			{
				last_url = cur_url;

				if(confirm("Perform check on " + cur_url + " ?"))
				{

					var searchUrl = 'http://0.0.0.0:8880/hello/' + cur_url ;
				    var x = new XMLHttpRequest();
					x.open('GET', searchUrl, true);

					x.onreadystatechange = function()
					{
    					if (x.readyState == XMLHttpRequest.DONE) 
    					{

    						var display = "This URL is " + x.responseText.substring(x.responseText.indexOf(':') + 1, x.responseText.indexOf('}'));
    						done = 1;
        					alert(display);
    					}
  					};
  

  					x.send();
  




				}
			}

			else
				done = 1;	
		}
			 
		if(done == 1)
			return {cancel:false};
		else
			return {cancel : true};
	},
	
	{ urls: ["<all_urls>"]},
	["blocking"]
);

