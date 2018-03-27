const fs = require('fs');

const data = fs.readFileSync(__dirname + "/data/train.json", 'utf8');

const arr = JSON.parse(data);

let output = "";

let min_1 = arr[0].band_1[0];
let max_1 = arr[0].band_1[0];
let min_2 = arr[0].band_2[0];
let max_2 = arr[0].band_2[0];

for (let i = 0; i < arr.length; i++) {
  const band1 = arr[i].band_1;
  for (let j = 0; j < band1.length; j++) {
    if (min_1 > band1[j]) {
      min_1 = band1[j];
    }

    if (max_1 < band1[j]) {
      max_1 = band1[j];
    }
  }

  const band2 = arr[i].band_2;
  for (let j = 0; j < band2.length; j++) {
    if (min_2 > band2[j]) {
      min_2 = band2[j];
    }

    if (max_2 < band2[j]) {
      max_2 = band2[j];
    }
  }
}

console.log('band_1 min: ', min_1);
console.log('band_1 max: ', max_1);
console.log('band_2 min: ', min_2);
console.log('band_2 max: ', max_2);
