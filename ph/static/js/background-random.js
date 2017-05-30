window.onload = function(){
	num = Math.floor(Math.random()*(5) + 1);
	document.getElementsByTagName("body")[0].style.backgroundImage = "url(../../static/bg/bg" + num + ".jpg)";
}