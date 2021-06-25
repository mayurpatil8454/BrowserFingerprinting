function collector() { 
var keys = []; 
 keys.push(navigator.userAgent);
 keys.push(navigator.language);
 keys.push(screen.colorDepth);
 //keys.push(typeof(window.openDatabase)); 
 //keys.push(navigator.cpuClass); 
 //keys.push(navigator.platform); 
 //falsecode();
 return keys;
}

function falsecode(){
	console.log("string");
}

