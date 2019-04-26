var T = [0];
var R = [0];
var B = [0];

for (var i = 0; i < 59; i++) {
  var newT = Math.max(...getTVals(i));
  var newR = Math.max(...getRVals(i));
  var newB = Math.max(...getBVals(i));
  T.push(newT);
  R.push(newR);
  B.push(newB);
}

function getTVals(i) {
  return [
    2 + 0.8 * (0.9 * T[i] + 0.1 * R[i]),
    3 + 0.8 * (0.7 * T[i] + 0.3 * R[i]),
  ];
}

function getRVals(i) {
  return [
    0.8 * (0.6 * R[i] + 0.3 * T[i] + 0.1 * B[i]),
    1 + 0.8 * (1 * B[i]),
  ];
}

function getBVals(i) {
  return [
    0.8 * (0.4 * B[i] + 0.6 * T[i]),
    1 + 0.8 * (B[i]),
  ];
}

console.log('----values----');
console.log('T values:', T);
console.log('R values:', R);
console.log('B values:', B);

console.log('----policies (D v. DD)----');
console.log('T:', getTVals(59));
console.log('R:', getRVals(59));
console.log('B:', getBVals(59));
