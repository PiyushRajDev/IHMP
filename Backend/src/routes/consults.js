const express = require("express");
const { syncOfflineConsults, getUnsyncedConsults } = require("../controllers/consultscontroller");

const router = express.Router();

// Sync offline consults to Supabase
router.post("/sync", syncOfflineConsults);

// Fetch all unsynced consults
router.get("/unsynced", getUnsyncedConsults);

module.exports = router;
