const supabase = require("../config/supabase.js");
const { v4: uuidv4 } = require("uuid");


// ✅ Sync Offline Consults to Supabase
const syncOfflineConsults = async (req, res) => {
    const { consults } = req.body;

    // Add UUIDs to each consult entry
    const formattedConsults = consults.map(consult => ({
        id: uuidv4(),
        doctor_id: consult.doctor_id,
        patient_id: consult.patient_id,
        notes: consult.notes,
        created_at: consult.created_at || new Date(),
        synced: true  // Mark as synced after adding to Supabase
    }));

    const { error } = await supabase.from("consults").insert(formattedConsults);

    if (error) return res.status(500).json({ error: error.message });

    res.json({ message: "Offline consults synced successfully" });
};

// ✅ Fetch All Unsynced Consults
const getUnsyncedConsults = async (req, res) => {
    const { data, error } = await supabase
        .from("consults")
        .select("*")
        .eq("synced", false);

    if (error) return res.status(500).json({ error: error.message });

    res.json(data);
};

module.exports = { syncOfflineConsults, getUnsyncedConsults };
