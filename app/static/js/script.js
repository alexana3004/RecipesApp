'use strict';
// let hasLicense = false;
// const passTest = true;
// if (passTest) hasLicenses =true;
// console.log(hasLicense)


// bill = prompt("Please enter the bill value: ");
// tip = bill > 50 && bill < 300 ? 0.15 : 0.20;
// console.log(`The total bill is $${Number(bill) + tip * Number(bill)}.`);

// alert("Hello!");

// if (2>3 || 3<2) {
//     console.log("Correct!")
// } else if (2 == "2"){
//     console.log(typeof "Incorrect!")
// }

// let variable = true;
// console.log(typeof variable);
// const variable = true;
// if (2<3) variable = false;
// console.log(String(variable));

// day = 'monday';
// switch (day) {
//     case 'monday':
//         console.log("monday")
//
//     case 'tuesday':
//         console.log("tuesday")
//         break;
//
//     default :
//         console.log("default")
// }

// const mark = {
//     firstName : 'Mark',
//     lastName : 'Miller',
//     mass : 78,
//     height : 1.69,
//     calcBMI: function () {
//         this.bmi = this.mass / this.height ** 2
//         return this.bmi
//     }
// };
//
// const john = {
//     firstName : 'John',
//     lastName: 'Smith',
//     mass: 92,
//     height: 1.95,
//     calcBMI: function () {
//         this.bmi = this.mass / this.height ** 2
//         return this.bmi
//     }
// };
//
// if (john.calcBMI() > mark.calcBMI()) {
//     console.log(`${john.firstName}'s BMI (${john.bmi.toFixed(1)}) is greater than ${mark.firstName}'s (${mark.bmi.toFixed(1)}).`)
// } else if (mark.bmi > john.bmi) {
//     console.log(`${mark.firstName}'s BMI (${mark.bmi.toFixed(1)}) is greater than ${john.firstName}'s (${john.bmi.toFixed(1)}).`)
// }

// const calcAvg = (a, b, c) => (a + b + c) / 3;
//
// const avgDolphins = calcAvg(85, 54, 41);
// const avgKoallas = calcAvg(23, 34, 27);
//
// function checkWinner(avgDolphins, avgKoallas) {
//     if (avgDolphins >= 2 * avgKoallas) {
//         console.log('Dolphins won!')
//     } else if (avgKoallas >= 2 * avgDolphins) {
//         console.log('Koallas won!')
//     } else {
//         console.log('No team won!')
//     }
// }
// checkWinner(avgDolphins, avgKoallas);

// const  calcTip = function (bill) {
//     return bill >= 50 && bill <= 300 ? bill * 0.15 : bill * 0.2
// }
//
// const bills = [125, 555, 44];
// const tips = new Array(calcTip(bills[0]), calcTip(bills[1]), calcTip(bills[2]));
// const totals = [bills[0] + tips[0], bills[1] + tips[1], bills[2] + tips[2]];
//
// console.log(tips, totals)