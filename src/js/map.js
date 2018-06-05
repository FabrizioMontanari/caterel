var map_text_data={
"1":["Partenza","Qui arriviamo in aereo."],
"2":["Prima tappa","Qui ci andiamo subito perché c'è il miglior ramen."],
"3":["Seconda tappa","Qua facciamo una breve sosta alle terme."],
"4":["Terza tappa","Qui c'è la statua gigante di Super Mario."],
"5":["Arrivo","Questo giro panoramico ci fa vistare tutti i villaggini."],
}

var map_image_map = {
	"1":"0",
	"2":"1",
	"3":"2-3",
	"4":"2-3",
	"5":"4-5-6-7",
	"6":"4-5-6-7",
	"7":"4-5-6-7",
	"8":"8",
	"9":"9",
	"10":"10-11",
	"11":"10-11",
	"12":"12-13-14-15-16-17-18",
	"13":"12-13-14-15-16-17-18",
	"14":"12-13-14-15-16-17-18",
	"15":"12-13-14-15-16-17-18",
	"16":"12-13-14-15-16-17-18",
	"17":"12-13-14-15-16-17-18",
	"18":"12-13-14-15-16-17-18",
	"19":"12-13-14-15-16-17-18",
	"20":"18",
}

function createImgUrl(step){
	if(window.location.href.indexOf('127.0.0.1')>=0)
		return '//127.0.0.1:8000/static/img/map/JMap-Day'+map_image_map[step]+'.png';
	else
		return '//static.imartinisisposano.it/img/map/JMap-Day'+map_image_map[step]+'.png';
}
function MapChange(btn){
	var step = $(btn).data("step");
	if ( step !=1 && $("#martini-gift__map__map").css('background-image').indexOf("JMap-Day0.png") !== -1){
		$("#martini-gift__map__map").addClass("zoomin");
		$("#martini-gift__map__map").removeClass("zoomout");
		setTimeout(function(){
								$("#martini-gift__map__map").css('background-image', 'url('+createImgUrl(step)+')');
								
							}, 500);
	}
	else{
		$("#martini-gift__map__map").css('background-image', 'url('+createImgUrl(step)+')');
		if (step==1){
			$("#martini-gift__map__map").removeClass("zoomin");
			$("#martini-gift__map__map").addClass("zoomout");
		}
	}
	$("#martini-gift__map__title").text(map_text_data[step][0]);
	$("#martini-gift__map__txt").text(map_text_data[step][1]);
}


$.fn.preload = function() {
	this.each(function(){
		$(".martini-preloader").append('<img src="'+this+'">');
	});
}

$(document).ready(function () {
	url_list=[];
	for (var i = 0; i < Object.keys(map_image_map).length; i++){
		url_list.push(createImgUrl(i+1));
	}
	
	$(url_list).preload();
	setTimeout(function(){
							$(".martini-preloader").addClass("hide");
						}, 500);
});