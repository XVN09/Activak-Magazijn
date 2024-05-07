const functions = require("firebase-functions");
const admin = require("firebase-admin");
// To avoid deployment errors, do not call admin.initializeApp() in your code

exports.newCloudFunction = functions
  .region("europe-central2")
  .https.onCall((data, context) => {
    const number = data.number;
    // Write your code below!
    function generateRandom13DigitNumber() {
      let thirteenDigitNumber = "";
      for (let i = 0; i < 13; i++) {
        thirteenDigitNumber += Math.floor(Math.random() * 10);
      }
      return thirteenDigitNumber;
    }

    let randomThirteenDigitNumber = generateRandom13DigitNumber();
    console.log(randomThirteenDigitNumber);

    // Write your code above!
    return "";
  });
