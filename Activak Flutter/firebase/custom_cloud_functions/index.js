const admin = require("firebase-admin/app");
admin.initializeApp();

const newCloudFunction = require("./new_cloud_function.js");
exports.newCloudFunction = newCloudFunction.newCloudFunction;
const generateRandomNumberStringOnCreate = require("./generate_random_number_string_on_create.js");
exports.generateRandomNumberStringOnCreate =
  generateRandomNumberStringOnCreate.generateRandomNumberStringOnCreate;
const updateUserBarcode = require("./update_user_barcode.js");
exports.updateUserBarcode = updateUserBarcode.updateUserBarcode;
