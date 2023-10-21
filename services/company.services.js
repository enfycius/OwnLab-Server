const config = require("../config.json");
const db = require("../helpers/db");
const Company = db.Company;

//retrieving user using id
async function getById(id) {
  console.log("finding id: ", id);
  return await Company.findById(id);
}

//adding user to db
async function create(companyParam) {
  //check if user exist
  const company = await Company.findOne({ company_name: companyParam.company_name });
  //validate
  if (user) throw `This email already exists: ${companyParam.company_name}`;

  //create user obj
  const newCompany = new Company(companyParam);

  await newCompany.save();
}

async function update(id, companyParam) {
  console.log(id, companyParam);
  const company = await Company.findById(id);
//   console.log(user.email, userParam.email);
  //validate the id and email
  if (!company) throw "User not found.";
  if (
    company.company_name !== companyParam.company_name &&
    (await Company.findOne({ company_name: companyParam.company_name }))
  ) {
    throw `User with email ${companyParam.company_name} already exist.`;
  }

  //copy the user obj
  Object.assign(company, companyParam);
  await company.save();
}

async function _delete(id) {
  await Company.findByIdAndRemove(id);
}

module.exports = {
  getById,
  create,
  update,
  delete: _delete,
};
