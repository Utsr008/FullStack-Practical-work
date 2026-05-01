// shortening Service 
//Build a URL shortening service using Express and MongoDB
//POST/shorturl accept a long url and return a shortened url
//Get/shortid redirect to original url and increment access count
//Patch/shortid allow updating longurl or access count


const express = require("express");
const mongoose = require("mongoose");
const app = express();
app.use(express.json());
mongoose.connect("");

const urlSchema = new mongoose.Schema({
  shortId: String,
  longUrl: String,
  accessCount: { type: Number, default: 0 }
});

const Url = mongoose.model("Url", urlSchema);

app.get("/", (req, res) => {
  res.send("URL Shortener Running");
});

app.post("/shorturl", async (req, res) => {
  const { longUrl } = req.body;

  const shortId = Math.random().toString(36).substring(2, 8);

  const data = await Url.create({
    shortId,
    longUrl
  });

  res.json({
    shortUrl: `http://localhost:3000/${data.shortId}`
  });
});


app.get("/:shortId", async (req, res) => {
  const data = await Url.findOne({ shortId: req.params.shortId });

  if (!data) return res.send("URL not found");

  data.accessCount++;
  await data.save();

  res.redirect(data.longUrl);
});
app.patch("/:shortId", async (req, res) => {
  const data = await Url.findOneAndUpdate(
    { shortId: req.params.shortId },
    req.body,
    { new: true }
  );
  if (!data) return res.send("Not found");
  res.json(data);
});
app.listen(3000, () => console.log("Server started on port 3000"));