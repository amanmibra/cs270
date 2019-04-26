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

console.log('***Question 2***');

console.log('----values----');
console.log('T values:', T);
console.log('R values:', R);
console.log('B values:', B);

console.log('----values for policies (D v. DD)----');
console.log('T:', getTVals(59));
console.log('R:', getRVals(59));
console.log('B:', getBVals(59));

console.log('***Question 3***');

var T = [0];
var R = [0];
var B = [0];

// 0 = drive, 1 = don't drive
var tPol = 1;
var rPol = 1;
var bPol = 1;

// convergence
var tConv = false;
var rConv = false;
var bConv = false;

// adding values of DD action
T.push(getTVals(0)[tPol]);
R.push(getRVals(0)[rPol]);
B.push(getBVals(0)[bPol]);

// index for loop
var index = 1;

while (!tConv || !rConv || !bConv) {
  var newT = Math.max(...getTVals(index));
  var newR = Math.max(...getRVals(index));
  var newB = Math.max(...getBVals(index));
  T.push(newT);
  R.push(newR);
  B.push(newB);

  if (!tConv && getTVals(index).indexOf(newT) == tPol) {
    tConv = true;
  } else {
    tPol = getTVals(index).indexOf(newT);
  }

  if (!rConv && getRVals(index).indexOf(newR) == rPol) {
    rConv = true;
  } else {
    rPol = getRVals(index).indexOf(newR);
  }

  if (!bConv && getBVals(index).indexOf(newB) == bPol) {
    bConv = true;
  } else {
    bPol = getBVals(index).indexOf(newB);
  }
  index++;
}

console.log('---values---');

console.log('T:', T);
console.log('R:',R);
console.log('B:', B);

console.log('---policies (0 for drive, 1 for don\'t drive)---');

console.log(tPol);
console.log(rPol);
console.log(bPol);
querySelector('query')
