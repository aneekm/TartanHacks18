function searchArtist(){
	var artistName = $("#searchfield").val()
	//var link = "/api/search_by_artist/" + artistName;
	var link = "templates/concerts_dummy_pittsburgh.json"
	var client = new HttpClient();
	client.get(link, function(response) {
    	var obj = JSON.parse(response);
	});	

	console.log(obj.resultsPage);
}

var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() { 
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }

        anHttpRequest.open( "GET", aUrl, true );            
        anHttpRequest.send( null );
    }
}