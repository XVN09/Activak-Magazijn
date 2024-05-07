const functions = require("firebase-functions");
const admin = require("firebase-admin");

const firestore = admin.firestore();

// Function to generate a random number string
function generateRandomNumberString(length) {
  let result = "";
  const characters = "0123456789";
  const charactersLength = characters.length;
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

// Cloud Function triggered upon user creation
exports.generateRandomNumberStringOnCreate = functions.auth
  .user()
  .onCreate(async (user) => {
    const { uid } = user;

    // Generate a random number string of length 6
    const randomNumberString = generateRandomNumberString(6);

    // Store the random number string in Firestore
    await firestore.collection("Users").doc(uid).set({
      Barcode: randomNumberString,
    });

    console.log(
      "Random number string generated and stored:",
      randomNumberString,
    );

    return null;
  });
