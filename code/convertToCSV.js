const fs = require('fs');
const stream = fs.createWriteStream('trainIceberg.csv');
const data = fs.readFileSync("./data/train.json");
const arr = JSON.parse(data);
const texture = fs.readFileSync("./data/texture.json");
const textureArr = JSON.parse(texture);

const add = function(output, feature) {
  if (feature === "na") {
    return output + ",";
  }

  return output + feature + ",";
}

stream.write('is_iceberg,id,inc_angle,ASM,');

for (let i = 0; i < 75*75*2; i++) {
  stream.write('F' + i + ',');
}

stream.write('\n');

for (let i = 0; i < arr.length; i++) {
  const entry = arr[i];

  let output = "";

  output = add(output, entry.is_iceberg);
  output = add(output, entry.id);
  output = add(output, entry.inc_angle);
  output = add(output, textureArr[i]);

  const band1 = entry.band_1;
  for (let j = 0; j < band1.length; j++) {
    output = add(output, band1[j])
  }

  const band2 = entry.band_2;

  for (let j = 0; j < band2.length; j++) {
    output = add(output, band2[j])
  }

  output += "\n";

  stream.write(output);
}
