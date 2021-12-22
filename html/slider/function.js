let body = document.body
let r = document.querySelector('#r')
let outputR = document.querySelector('#outputR')
let hexVal_out = document.querySelector('#hexVal')
 
function setColor(){
  let rHexVal = parseInt(r.value, 10).toString(16)
  let gHexVal = parseInt(r.value, 10).toString(16)
  let bHexVal = parseInt(r.value, 10).toString(16)
  let hexVal = "#" + pad(rHexVal) + pad(gHexVal) + pad(bHexVal)
  
  body.style.backgroundColor = hexVal;
  hexVal_out.value = hexVal;
}
 
function pad(n){
  return (n.length<2) ? "0"+n : n;
}
 
r.addEventListener('input', () => {
  setColor();
  outputR.value = r.value;
}, false);
