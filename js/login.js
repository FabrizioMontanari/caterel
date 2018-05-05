/*login dei poveri*/
function checkLogin(username,password){
	if (username === "nomeutente" && password==="password"){
		console.log("credenziali riconosciute");
		return true;
	}
	if (username==="ellie" && password==="tvtb"){
		enableHearts();
		console.log("AMMMOREEEE");
		return true;
	}
	console.log("credenziali non riconosciute");
	return false;
}

function loginSuccessUptadeUI(){
	$(".login-content").addClass("hide");
	$(".site-content").removeClass("hide");
}

function onAccediClick(){
	var u=$("#username").val();
	var p=$("#password").val();
	if (checkLogin(u,p)){
		setCookie("login_done","t");
		loginSuccessUptadeUI();
	}
}

function landingLoginCheck(){
	var credential = getUrlVars();
	console.log("found this cookie: " +getCookie("login_done"));
	console.log("check cookie: " +getCookie("login_done")!=="t");
	if ( !(credential.hasOwnProperty('password') && credential.hasOwnProperty('username')) && getCookie("login_done")!=="t" ) {
		return;
	}
	else{
		if (checkLogin(credential["username"],credential["password"]) || getCookie("login_done")==="t"){
			setCookie("login_done","t");
			loginSuccessUptadeUI();
		}
	}
}
// Read a page's GET URL variables and return them as an associative array.
function getUrlVars(){
	var vars = [], hash;
	var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
	for(var i = 0; i < hashes.length; i++){
		hash = hashes[i].split('=');
		vars.push(hash[0]);
		vars[hash[0]] = hash[1];
	}
	return vars;
}

function setCookie(cname, cvalue) {
	var ctmp = cname + "="+ cvalue;
	document.cookie = ctmp;
	console.log("cookie set: "+ ctmp);
}

function getCookie(cname) {
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i = 0; i < ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}

function enableHearts(){
	$(".site-content").append("<div id='heart1' class='heart'></div><div id='heart2' class='heart'></div><div id='heart3' class='heart'></div><div id='heart4' class='heart'></div>");
}

$(document).ready(function () {
	landingLoginCheck();
});