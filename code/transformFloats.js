const fs = require('fs');

const data = fs.readFileSync("data/train.json", 'utf8');

const arr = JSON.parse(data);

let output = "";
let output2 = "";

for (let i = 0; i < arr.length; i++) {
  const band1 = arr[i].band_1;
  for (let j = 0; j < band1.length; j++) {
    band1[j] = Math.round((band1[j] + 50) * 255 / 100);
  }

  output += band1.join(" ");
  output += " " + arr[i].is_iceberg + " ";

  const band2 = arr[i].band_2;
  for (let j = 0; j < band2.length; j++) {
    band2[j] = Math.round((band2[j] + 50) * 255 / 100);
  }

  output2 += band2.join(" ");
  output2 += " " + arr[i].is_iceberg + " ";
}


fs.writeFile('./pixels.txt', output, (err) => {
  if (err) throw err;
  console.log('pixels.txt has been saved!');
});

fs.writeFile('./pixels2.txt', output, (err) => {
  if (err) throw err;
  console.log('pixels2.txt has been saved!');
});
