const express = require("express");
const { addMedicalData, fetchMedicalData } = require("../controllers/medicalDataController");
const router = express.Router();

router.post("/", addMedicalData);
router.get("/:patientId", fetchMedicalData);

export default router;
