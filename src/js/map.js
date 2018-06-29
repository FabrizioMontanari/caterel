/*var map_text_data={
"1":["Partenza","Qui arriviamo in aereo."],
"2":["Prima tappa","Qui ci andiamo subito perché c'è il miglior ramen."],
"3":["Seconda tappa","Qua facciamo una breve sosta alle terme."],
"4":["Terza tappa","Qui c'è la statua gigante di Super Mario."],
"5":["Arrivo","Questo giro panoramico ci fa vistare tutti i villaggini."],
}*/

var current_step = 0;

var map_image_map = {
	"1":"1",
	"2":"2-3",
	"3":"2-3",
	"4":"4-5-6-7",
	"5":"4-5-6-7",
	"6":"4-5-6-7",
	"7":"4-5-6-7",
	"8":"8",
	"9":"9",
	"10":"10-11",
	"11":"10-11",
	"12":"12-13-14-15-16-17",
	"13":"12-13-14-15-16-17",
	"14":"12-13-14-15-16-17",
	"15":"12-13-14-15-16-17",
	"16":"12-13-14-15-16-17",
	"17":"12-13-14-15-16-17",
	"18":"18",
}

function createImgUrl(step){
	if(window.location.href.indexOf('127.0.0.1')>=0)
		return '//127.0.0.1:8000/static/img/map/JMap-Day'+map_image_map[step]+'.png';
	else
		return '//static.imartinisisposano.it/img/map/JMap-Day'+map_image_map[step]+'.png';
}
function MapChange(btn){
	doMapChange(btn);
}

function doMapChange(btn){
	var step = $(btn).data("step");
	current_step = step;
	if ( step !=0 && $("#martini-gift__map__map").css('background-image').indexOf("JMap-Day0.png") !== -1){
		$("#martini-gift__map__map").addClass("zoomin");
		$("#martini-gift__map__map").removeClass("zoomout");
		setTimeout(function(){
								$("#martini-gift__map__map").css('background-image', 'url('+createImgUrl(step)+')');
								
							}, 500);
	}
	else{
		$("#martini-gift__map__map").css('background-image', 'url('+createImgUrl(step)+')');
		if (step==0){
			$("#martini-gift__map__map").removeClass("zoomin");
			$("#martini-gift__map__map").addClass("zoomout");
		}
	}
	$("#martini-gift__map__title").text(map_text_data[step][0]);
	$("#martini-gift__map__txt").text(map_text_data[step][1]);

	$(".martini-gift__controls__btn").removeClass("selected_day");
	$(btn).addClass("selected_day");
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

function onMapClick(){
	if (current_step <18) current_step++; 
	btn = $(".martini-gift__controls__btn[data-step=" + current_step + "]");
	console.log(btn);
	doMapChange(btn);
}