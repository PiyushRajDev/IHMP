const supabase = require("../config/supabase");

exports.createMedicalData = async (patientId, data) => {
  return await supabase
    .from("medical_data")
    .insert([{ patient_id: patientId, data }]);
};

exports.getMedicalData = async (patientId) => {
  return await supabase
    .from("medical_data")
    .select("*")
    .eq("patient_id", patientId);
};
