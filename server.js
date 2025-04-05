const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();

// ✅ Cho phép mọi domain gọi API này
app.use(cors());

app.get("/", (req, res) => {
  res.send("Transcript API đang hoạt động!");
});

// ✅ Endpoint chính để lấy phụ đề
app.get("/transcript/:videoId", async (req, res) => {
  const { videoId } = req.params;

  try {
    const response = await axios.get(`https://video.google.com/timedtext?lang=en&v=${videoId}`);
    const xml = response.data;

    // Dùng regex tách text từ XML
    const lines = [...xml.matchAll(/<text.+?>(.*?)<\/text>/g)].map(match =>
      match[1]
        .replace(/&amp;/g, "&")
        .replace(/&#39;/g, "'")
        .replace(/&quot;/g, '"")
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

// ✅ Chạy app
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Transcript API đang chạy tại http://localhost:${PORT}`);
});
