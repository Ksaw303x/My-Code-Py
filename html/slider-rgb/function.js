let h = document.querySelector('#r')
let outputH = document.querySelector('#outputR')
let saturation = document.querySelector('#saturation')
let outputSaturation = document.querySelector('#outputSaturation')
let light = document.querySelector('#light')
let outputLight = document.querySelector('#outputLight')

let hexVal_out = document.querySelector('#hexVal')

let hueValue = 30
let saturationValue = 70
let lightValue = 50


h.value = hueValue

saturation.value = saturationValue
outputSaturation.value = saturationValue
light.value = lightValue
outputLight.value = lightValue


const HSLToRGB = (h, s, l) => {
  s /= 100;
  l /= 100;
  const k = n => (n + h / 30) % 12;
  const a = s * Math.min(l, 1 - l);
  const f = n =>
    l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));
  return [255 * f(0), 255 * f(8), 255 * f(4)];
};

function updateColor(){
  let colorHexVal = "#"
  let color = HSLToRGB(hueValue, lightValue, saturationValue)
  color.forEach((value) => {
    colorHexVal += parseInt(value, 10).toString(16).padStart(2, "0")
  })

  document.body.style.backgroundColor = colorHexVal;
  hexVal_out.value = colorHexVal;
}
 
h.addEventListener('input', () => {
  outputH.value = hueValue = h.value;
  updateColor()
}, false);

light.addEventListener('input', () => {
  outputLight.value = lightValue = light.value;
  updateColor()
}, false);

saturation.addEventListener('input', () => {
  saturationLight.value = saturationValue = saturation.value;
  updateColor()
}, false);


updateColor()
