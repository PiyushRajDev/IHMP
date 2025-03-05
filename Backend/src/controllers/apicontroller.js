import { v4 as uuidv4 } from "uuid";  
import supabase from "../config/supabase.js";  // Correct path to supabase.js  

// ✅ Add a New Patient  
export const addPatient = async (req, res) => {  
    const { name, birthdate } = req.body;  
    const id = uuidv4(); // Generate a UUID for the patient  

    // Insert the new patient into the patients table  
    const { error } = await supabase.from("patients").insert([{ id, name, birthdate }]);  

    if (error) {  
        return res.status(500).json({ error: error.message });  
    }  

    res.status(201).json({ message: "Patient added successfully", id });  
};  

// ✅ Fetch All Patients  
export const fetchPatients = async (_, res) => {  
    const { data, error } = await supabase.from("patients").select("*");  

    if (error) {  
        return res.status(500).json({ error: error.message });  
    }  

    res.json(data);  
};  

// ✅ Add Medical Data for a Patient  
export const addMedicalData = async (req, res) => {  
    const { patient_id, data } = req.body; // Changed patientId to patient_id for consistency  
    const id = uuidv4(); // Generate a UUID for the medical data record  

    // Insert the new medical data into the medical_data table  
    const { error } = await supabase.from("medical_data").insert([{ id, patient_id, data }]);  

    if (error) {  
        return res.status(500).json({ error: error.message });  
    }  

    res.status(201).json({ message: "Medical data stored successfully", id });  
};  

// ✅ Fetch Medical Data for a Patient  
export const fetchMedicalData = async (req, res) => {  
    const { patientId } = req.params;  

    const { data, error } = await supabase  
        .from("medical_data")  
        .select("*")  
        .eq("patient_id", patientId);  

    if (error) {  
        return res.status(500).json({ error: error.message });  
    }  

    res.json(data);  
};  