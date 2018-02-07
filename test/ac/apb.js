let readline = require('readline');
let rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

rl.on('line', s => {
	let a = s.split(' ').map(x => parseInt(x));
	console.log(a[0] + a[1]);
});