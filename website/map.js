var map_text_data={
"1":["Partenza","Qui arriviamo in aereo."],
"2":["Prima tappa","Qui ci andiamo subito perché c'è il miglior ramen."],
"3":["Seconda tappa","Qua facciamo una breve sosta alle terme."],
"4":["Terza tappa","Qui c'è la statua gigante di Super Mario."],
"5":["Arrivo","Questo giro panoramico ci fa vistare tutti i villaggini."],
}

function createImgUrl(step){
	return 'https://raw.githubusercontent.com/FabrizioMontanari/caterel/master/0'+step+'.png';
}
function MapChange(btn){
	var step = $(btn).data("step");
	if ( step !=1 && $("#martini-gift__map__map").css('background-image').toLowerCase() == 'url("https://raw.githubusercontent.com/FabrizioMontanari/caterel/master/01.png")'.toLowerCase()){
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
	$([createImgUrl(1),createImgUrl(2),createImgUrl(3),createImgUrl(4),createImgUrl(5)]).preload();
	setTimeout(function(){
							$(".martini-preloader").addClass("hide");
						}, 500);
});