const functions = require("firebase-functions");
const admin = require("firebase-admin");

admin.initializeApp();

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

// Cloud Function triggered upon user document creation or update
exports.updateUserBarcode = functions.firestore
  .document("users/{userId}")
  .onCreate(async (snapshot, context) => {
    const userData = snapshot.data();

    // Check if the user document doesn't have a Barcode field
    if (!userData.Barcode) {
      // Generate a random barcode
      const randomBarcode = generateRandomNumberString(6);

      // Update the user document with the generated barcode
      await snapshot.ref.update({
        Barcode: randomBarcode,
      });

      console.log(
        `Barcode generated and updated for user: ${context.params.userId}`,
      );
    }

    return null;
  });

// To avoid deployment errors, do not call admin.initializeApp() in your code
