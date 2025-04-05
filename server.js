const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
app.use(cors());

app.get("/transcript/:videoId", async (req, res) => {
  const { videoId } = req.params;
  try {
    const response = await axios.get(`https://video.google.com/timedtext?lang=en&v=${videoId}`);
    const xml = response.data;

    // Dùng regex để tách text từ XML (đơn giản)
    const lines = [...xml.matchAll(/<text.+?>(.*?)<\/text>/g)].map(match =>
      match[1].replace(/&amp;/g, "&").replace(/&#39;/g, "'").replace(/&quot;/g, '"')
    );
    const fullText = lines.join(" ");

    res.json({ text: fullText });
  } catch (err) {
    res.status(500).json({ error: "Không lấy được transcript!" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Transcript API đang chạy tại http://localhost:${PORT}`);
});
