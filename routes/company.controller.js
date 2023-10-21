const express = require("express");
const router = express.Router();
const userServices = require("../services/company.services");

//routes
router.post("/register", register);
router.get("/:id", getById);
router.put("/:id", update);
router.delete("/:id", _delete);


function register(req, res, next) {
  userServices
    .create(req.body)
    .then((user) =>
      res.json({
        user: user,
        message: `User Registered successfully with email ${req.body.email}`,
      })
    )
    .catch((error) => next(error));
}

// function getAll(req, res, next) {
//   const currentUser = req.user;

//   if (currentUser.role !== Role.Admin) {
//     return res.status(401).json({ message: "Not Authorized!" });
//   }
//   userServices
//     .getAll()
//     .then((users) => res.json(users))
//     .catch((err) => next(err));
// }

function getById(req, res, next) {
  userServices
    .getById(req.params.id)
    .then((user) => {
      if (!user) {
        res.status(404).json({ message: "User Not Found!" });
        next();
      }
      return res.json(user);
    })
    .catch((error) => next(error));
}

function update(req, res, next) {
  userServices
    .update(req.params.id, req.body)
    .then(() =>
      res.json({
        message: `User with id: ${req.params.id} updated successfully.`,
      })
    )
    .catch((error) => next(error));
}

function _delete(req, res, next) {
  userServices
    .delete(req.params.id)
    .then(() =>
      res.json({
        message: `User with id: ${req.params.id} deleted successfully.`,
      })
    )
    .catch((error) => next(error));
}

module.exports = router;