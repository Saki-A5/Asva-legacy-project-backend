import express from "express";
// import dbConn from "./api/db/db.js";
import dotenv from "dotenv";
import cors from "cors";

dotenv.config();
dbConn();

import route from "./api/routes/index.js";

const app = express();
app.use(cors());
app.use(express.json());
app.use(route);

app.get("/", (req, res) => {
    res.send("welcome, thanks for considering us");
});

const port = process.env.PORT;

app.listen(port, "localhost", () => console.log(`live now on port ${port}`));