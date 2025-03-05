import express from "express";  
import cors from "cors";  
import dotenv from "dotenv";  
import apiRoutes from "./src/routes/api.js";  // Updated path  
import consultsRoutes from "./src/routes/consults.js"; // Import the consults routes  
dotenv.config();  // Load environment variables  

const app = express();  
app.use(cors());  
app.use(express.json());  

app.use("/api/consults", consultsRoutes); // Use the imported consultsRoutes  
app.use("/api", apiRoutes);  // Attach your routes here  

const PORT = process.env.PORT || 3000;  // Use environment variable or default  
app.listen(PORT, () => {  
    console.log(`Server running on http://localhost:${PORT}`);  
});  