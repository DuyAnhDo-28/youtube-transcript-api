const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
app.use(cors());

app.get("/", (req, res) => {
  res.send("Transcript API đang hoạt động!");
});

app.get("/transcript/:videoId", async (req, res) => {
  const { videoId } = req.params;
  const lang = req.query.lang || "en"; // Cho phép đổi ngôn ngữ

  try {
    const response = await axios.get(`https://video.google.com/timedtext?lang=${lang}&v=${videoId}`);
    const xml = response.data;

    const matches = [...xml.matchAll(/<text.+?>(.*?)<\/text>/g)];
    if (matches.length === 0) {
      return res.status(404).json({
        error: `Không tìm thấy phụ đề cho video '${videoId}' với ngôn ngữ '${lang}'.`,
        suggestion: "Thử với video khác hoặc thêm ?lang=vi nếu có phụ đề tiếng Việt."
      });
    }

    const lines = matches.map(match =>
      match[1]
        .replace(/&amp;/g, "&")
        .replace(/&#39;/g, "'")
        .replace(/&quot;/g, '"')
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">")
    );

    const fullText = lines.join(" ");
    res.json({ text: fullText });

  } catch (err) {
    console.error("Lỗi lấy transcript:", err.message);
    res.status(500).json({ error: "Không thể lấy transcript cho video này." });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Transcript API đang chạy tại http://localhost:${PORT}`);
});
