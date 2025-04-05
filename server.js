const express = require("express");
const cors = require("cors");
const { YoutubeTranscript } = require("youtube-transcript");

const app = express();
app.use(cors());

app.get("/transcript/:videoId", async (req, res) => {
  const { videoId } = req.params;
  try {
    const transcript = await YoutubeTranscript.fetchTranscript(videoId);
    const fullText = transcript.map(x => x.text).join(" ");
    res.json({ text: fullText });
  } catch (err) {
    res.status(500).json({ error: "Không lấy được transcript." });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Transcript API chạy tại http://localhost:${PORT}`);
});
