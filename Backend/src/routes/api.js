import express from "express";
import { addPatient, fetchPatients, addMedicalData, fetchMedicalData } from "../controllers/apiController.js";

const router = express.Router();

// Routes for patients
router.post("/patients", addPatient);
router.get("/patients", fetchPatients);

// Routes for medical data
router.post("/medical-data", addMedicalData);
router.get("/medical-data/:patientId", fetchMedicalData);

export default router;
