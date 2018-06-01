/*utilities*/
function escape(txt){
	return $("<div>").text(txt).html();
}
function toTitleCase(str) {
	return str.replace(/\w\S*/g, function(txt){
		return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
	});
}
/*fine utilities*/

/**
 * Preparo il contenuto e mostro l'overlay
 */
function onConfirmClick(){
	fillConfirmation();
	$("#confirm-overlay").removeClass("hide");
}
/**
 * Costruisco tutti gli elementi dell'overlay leggendo i campi compilati dall'utente
 */
function fillConfirmation(){
	var overlay = $("#confirm-overlay");
	overlay.empty();
	var overlay_content = '<h1 class="martini-confirm__container__overlay__title">confermi la presenza di</h1>\n';
	overlay_content += '<p class="martini-confirm__container__overlay__member">'+toTitleCase(escape($('input[name=main_nome]').val()))+' '+toTitleCase(escape($('input[name=main_cognome]').val()))+', menu '+$('select[name=main_menu]').val()+'</p>\n';
	

	$('div[id*="familiare_"][id$="_confirmed"]').each(function(i){
		if ($( this ).hasClass('checked')){
			overlay_content += '<p class="martini-confirm__container__overlay__member">'+toTitleCase(escape($('input[name=familiare_'+i+'_nome]').val()))+', menu '+$('select[name=familiare_'+i+'_menu]').val()+'</p>\n';
		}
	});
		
	overlay_content += '<div class="martini-confirm__container__overlay__submit">CONFERMA</div>\
						<div class="martini-confirm__container__overlay__back" onclick="onBackClick()">MODIFICA</div>';
	overlay.append(overlay_content);
	return
}
/**
 * Riempe la sezione famiglia.
 * acceta una array di nomi dei familiari es: ["Marco Baldo", "Bella Lui", "Topo Gigio"]
 */
function fillFamily(family){
	if(!Array.isArray(family)){
		console.log("Errore: l'argomento non è un array");
		return;
	}
	var container = $('#martini-confirm__container__family');
	container.empty();
	family.forEach(function(member, i){
		var new_element = '<div id="familiare_'+i+'" class="martini-confirm__container__family__member col-sm-5">\
					<div class="martini-confirm__container__family__member__name">\
						<input type="text" name="familiare_'+i+'_nome" value="'+member+'" readonly>\
						<div id="familiare_'+i+'_confirmed" class="checkbox" onclick="$(this).toggleClass(\'checked\')">&nbsp;</div>\
					</div>\
					<p>menu</p>\
					<select name="familiare_'+i+'_menu">\
						<option>regular</option>\
						<option>vegetariano</option>\
						<option>intollerante al lattosio</option>\
						<option>celiaco</option>\
						<option>vegano</option>\
					</select>\
				</div>';
		container.append(new_element);
	});
	
}

function onBackClick(){
	$("#confirm-overlay").addClass("hide");
}