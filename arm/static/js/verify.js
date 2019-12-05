//Asset capture barcode scanner

if(window.location.hash.substr(1,2) == "zx"){
	var bc = window.location.hash.substr(3);
	localStorage["barcode"] = decodeURI(window.location.hash.substr(3))
	window.close();
	self.close();
	window.location.href = "about:blank";//In case self.close isn't allowed
}

var changingHash = false;
function onbarcode(event){
	switch(event.type){
		case "hashchange":{
			if(changingHash == true){
				return;
			}
			var hash = window.location.hash;
			if(hash.substr(0,3) == "#zx"){
				hash = window.location.hash.substr(3);
				changingHash = true;
				window.location.hash = event.oldURL.split("\#")[1] || ""
				changingHash = false;
				verifiedBarcode(hash);
			}

			break;
		}
		case "storage":{
			window.focus();
			if(event.key == "barcode"){
				window.removeEventListener("storage", onbarcode, false);
				verifiedBarcode(event.newValue);
			}
			break;
		}
		default:{
			console.log(event)
			break;
		}
	}
}
window.addEventListener("hashchange", onbarcode, false);

function code2Verify(){
	var href = window.location.href;
	var ptr = href.lastIndexOf("#");
	if(ptr>0){
		href = href.substr(0,ptr);
	}
	window.addEventListener("storage", onbarcode, false);
	setTimeout('window.removeEventListener("storage", onbarcode, false)', 15000);
	localStorage.removeItem("barcode");
	//window.open  (href + "#zx" + new Date().toString());

	if(navigator.userAgent.match(/Firefox/i)){
		//Used for Firefox. If Chrome uses this, it raises the "hashchanged" event only.
		window.location.href =  ("zxing://scan/?ret=" + encodeURIComponent(href + "#zx{CODE}"));
	}else{
		//Used for Chrome. If Firefox uses this, it leaves the scan window open.
		window.open   ("zxing://scan/?ret=" + encodeURIComponent(href + "#zx{CODE}"));
	}
}

function verifiedBarcode(bc){
	document.getElementsByName("barcode").value = bc;
}