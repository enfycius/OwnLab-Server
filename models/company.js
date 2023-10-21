const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const companySchema = new Schema({
  company_name: { type: String, required: true },
  postcode: { type: String, required: true },
  address: { type: String, required: true },
  detail_address: { type: String, required: true },
  ceo_name: { type: String, required: true },
  tel: { type: String, required: true},
});

schema.set("toJSON", {
  virtuals: true,
  versionKey: false,
  transform: function (doc, ret) {
    delete ret._id, delete ret.password;
  },
});

module.exports = mongoose.model("Company", companySchema);
