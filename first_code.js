var readline = require('readline-sync');
var nome = readline.question("Qual o seu nome? ");
var numero = readline.questionFloat("digite um numero: ");
var numero2 = readline.questionFloat("digite um numero: ");
var soma = numero + numero2;

console.log(`O nome informado foi ${nome} e a soma é ${soma}`);