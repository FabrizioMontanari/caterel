function escape(txt) {
	return $('<div>').text(txt).html();
}

function toTitleCase(str) {
	return str.replace(/\w\S*/g, function (txt) {
		return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
	});
}


function getFieldValue(fieldName, type) {
	var fieldType = type || 'input';
	return escape($(fieldType + '[name=' + fieldName + ']').val().trim());
}

/**
 * Preparo il contenuto e mostro l'overlay
 */
function onCiSaroClick() {
	fillConfirmation();
	$('#confirm-overlay').removeClass('hide');
}

/**
 * Costruisco tutti gli elementi dell'overlay leggendo i campi compilati dall'utente
 */
function fillConfirmation() {
	var overlay = $('#confirm-overlay');
	overlay.empty();
	var overlay_content = '<h1 class="martini-confirm__container__overlay__title">confermi la presenza di</h1>\n';
	overlay_content += '<p class="martini-confirm__container__overlay__member">' + toTitleCase(escape($('input[name=main_nome]').val())) + ' ' + toTitleCase(escape($('input[name=main_cognome]').val())) + ', menu ' + $('select[name=main_menu]').val() + '</p>\n';

	$('div[id*="familiare_"][id$="_confirmed"]').each(function (i) {
		if ($(this).hasClass('checked')) {
			overlay_content += '<p class="martini-confirm__container__overlay__member">' + toTitleCase(escape($('input[name=familiare_' + i + '_nome]').val())) + ', menu ' + $('select[name=familiare_' + i + '_menu]').val() + '</p>\n';
		}
	});

	overlay_content += '<div class="martini-confirm__container__overlay__submit" onclick="onConfermaClick();">CONFERMA</div>\
						<div class="martini-confirm__container__overlay__back" onclick="onBackClick();">MODIFICA</div>';
	overlay.append(overlay_content);
}

/**
 * Riempe la sezione famiglia.
 * acceta una array di nomi dei familiari es: ["Marco Baldo", "Bella Lui", "Topo Gigio"]
 * In caso di +1 viene aggiunto un solo membro e si inserisce un inputfield hidden
 */
function fillFamily(family) {
	var container = $('#martini-confirm__container__family');
	container.empty();
	family.forEach(function (member, i) {
		var name_input = member ? '<input type="text" name="familiare_' + i + '_nome" value="' + toTitleCase(member) + '" readonly>' :
			'<input type="text" name="familiare_' + i + '_nome" value="" placeholder="Nome e Cognome">\
								   <input type="hidden" name="plus_one" value="plus_one_' + i + '">'

		var new_element = '<div id="familiare_' + i + '" class="martini-confirm__container__family__member col-sm-5">\
					<div class="martini-confirm__container__family__member__name">\
						'+ name_input + '\
						<div id="familiare_'+ i + '_confirmed" class="checkbox" onclick="$(this).toggleClass(\'checked\')">&nbsp;</div>\
					</div>\
					<p>Menu</p>\
					<select name="familiare_'+ i + '_menu">\
						<option>Normale</option>\
						<option>Celiaco</option>\
						<option>Intollerante al Lattosio</option>\
						<option>Bimbi</option>\
						<option>Vegetariano</option>\
						<option>Vegano</option>\
					</select>\
				</div>';
		container.append(new_element);
	});

}

function onBackClick() {
	$('#confirm-overlay').addClass('hide');
}

/**
 * invia la richiesta per verificare la presenza dell'invitato nella lista e gestisce la risposta.
 * Se l'utente esiste si mostrano le opzioni da compilare e gli eventuali familiari
 */
function onUserNomeCognomeEntered() {
	var nome = getFieldValue('main_nome');
	var cognome = getFieldValue('main_cognome');
	var guestFullName = nome + ' ' + cognome;

	//prevent request when empty
	if (nome === '' || cognome === '') {
		return;
	}
	if (nome.toLowerCase() === 'ellie' || cognome.toLowerCase() === 'ellie') {
		enableHearts();
		return;
	}

	//prevent request when already checked
	if ($('#checkbox_main').hasClass('checked') || $('#checkbox_main').hasClass('checking')) {
		return;
	}


	$('#checkbox_main').addClass('checking');
	$.get('/get_family', { guestFullName: guestFullName })
		.done(function (data) {
			if (!data.guestAllowed) {
				//remove checking status
				$('#checkbox_main').removeClass('checking');

				$('#not_invited').removeClass('hide');
				$('#select_your_menu_text').addClass('hide');
				$('#select_main_menu').addClass('hide');
				$('#conferma_cari_text').addClass('hide');
				$('#extra_notes_text').addClass('hide');
				$('#martini-confirm__container__family').addClass('hide');
				$('#main-email-label').addClass('hide');
				$('#main-email').addClass('hide');
				$('#notes').addClass('hide');
				$('#confirm-be-there').addClass('hide');

				return;
			}

			//lock curent user
			$('input[name=main_nome]').prop('readonly', true);
			$('input[name=main_cognome]').prop('readonly', true);
			//remove checking status
			$('#checkbox_main').removeClass('checking');
			//check flag
			$('#checkbox_main').addClass('checked');

			//show fields
			$('#not_invited').addClass('hide');
			$('#select_your_menu_text').removeClass('hide');
			$('#select_main_menu').removeClass('hide');
			$('#extra_notes_text').removeClass('hide');
			$('#martini-confirm__container__family').removeClass('hide');
			$('#main-email-label').removeClass('hide');
			$('#main-email').removeClass('hide');
			$('#notes').removeClass('hide');
			$('#confirm-be-there').removeClass('hide');

			if (data.guestFamily.length) {
				$('#conferma_cari_text').removeClass('hide');
			}

			fillFamily(data.guestFamily);
		}).fail(function (jqXHR, textStatus) {
			displayOverlayMessage('Errore durante il caricamento della lista invitati!<br />Prova più tardi, o contattaci direttamente!');
		});
}


/**
 * invia i dati della prenotazione
 */
function displayOverlayMessage(message) {
	var overlay = $('#confirm-overlay');

	overlay.empty();
	var overlay_content = '<h2 class="martini-confirm__container__overlay__title">' + message + '</h2>';
	overlay.append(overlay_content);
}

function onConfermaClick() {
	var guestFullName = getFieldValue('main_nome') + ' ' + getFieldValue('main_cognome')

	family = [{
		nome: guestFullName,
		email: getFieldValue('main_email'),
		menu: getFieldValue('main_menu', 'select'),
		nota: getFieldValue('note', 'textarea')
	}]

	$('div[id*="familiare_"][id$="_confirmed"]').each(function (i) {
		if ($(this).hasClass('checked')) {
			member = {
				'nome': escape($('input[name=familiare_' + i + '_nome]').val()),
				'menu': $('select[name=familiare_' + i + '_menu]').val(),
			};
			is_plus_one = $('input[name=plus_one][type=hidden]').length == 1;
			if (is_plus_one) {
				member.is_plusone_of = guestFullName;
			}
			family.push(member);
		}
	});

	displayOverlayMessage('Conferma in corso...Attendere prego');
	$.ajax({
		type: 'POST',
		url: '/confirmation',
		cache: false,
		data: JSON.stringify({ family: family }),
		contentType: 'application/json; charset=utf-8',
	}).done(function (data) {
		displayOverlayMessage('Fatto il misfatto!');
	}).fail(function (jqXHR, textStatus) {
		displayOverlayMessage('Conferma Fallita!<br />Prova più tardi, o contattaci direttamente!');
	});
}

/*for the lulz*/
function enableHearts() {
	$("body").append("<div id='heart1' class='heart'></div><div id='heart2' class='heart'></div><div id='heart3' class='heart'></div><div id='heart4' class='heart'></div>");
}

$(document).ready(function () {
	$(".martini-confirm__container__cognome").keypress(function (e) {
		if (e.which == 13) {
			onUserNomeCognomeEntered();
		}
	});
});