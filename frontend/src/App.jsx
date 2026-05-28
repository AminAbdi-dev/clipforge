import { useState } from "react";

function App() {

  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [video, setVideo] = useState("");

  const handleGenerate = async () => {

    if (!url) return;

    setLoading(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/process/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            youtube_url: url,
          }),
        }
      );

      const data = await response.json();

      console.log(data.final_video);

      setVideo(
        `http://127.0.0.1:8000/media${data.final_video}`
      );
    } catch (error) {

      console.log(error);

    }

    setLoading(false);
  };

  return (

    <div className="min-h-screen bg-[#07070a] text-white overflow-hidden">

      {/* TOP GLOW */}
      <div className="absolute top-[-200px] left-1/2 -translate-x-1/2 w-[700px] h-[700px] bg-purple-700 opacity-20 blur-[180px]" />

      {/* CONTENT */}
      <div className="relative z-10 max-w-6xl mx-auto px-6 py-20">

        {/* HERO */}
        <div className="text-center">

          <h1 className="text-7xl font-black tracking-tight bg-gradient-to-r from-white to-purple-400 bg-clip-text text-transparent">
            ClipForge
          </h1>

          <p className="text-zinc-400 mt-6 text-xl max-w-2xl mx-auto leading-relaxed">
            Transform long YouTube videos into viral AI-generated shorts with automatic clipping and subtitles.
          </p>

        </div>

        {/* INPUT CARD */}
        <div className="mt-16 bg-[#111113] border border-zinc-800 rounded-3xl p-8 shadow-2xl">

          <div className="flex flex-col md:flex-row gap-4">

            <input
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Paste YouTube URL..."
              className="flex-1 bg-[#1a1a1d] border border-zinc-700 rounded-2xl px-6 py-4 text-white outline-none focus:border-purple-500"
            />

            <button
              onClick={handleGenerate}
              className="bg-purple-600 hover:bg-purple-500 transition-all rounded-2xl px-8 py-4 font-semibold"
            >
              Generate Short
            </button>

          </div>

          {/* FEATURES */}
          <div className="flex flex-wrap gap-3 mt-6">

            <div className="bg-zinc-900 border border-zinc-800 px-4 py-2 rounded-full text-sm text-zinc-300">
              AI Hook Detection
            </div>

            <div className="bg-zinc-900 border border-zinc-800 px-4 py-2 rounded-full text-sm text-zinc-300">
              Auto Subtitles
            </div>

            <div className="bg-zinc-900 border border-zinc-800 px-4 py-2 rounded-full text-sm text-zinc-300">
              Viral Clips
            </div>

          </div>

        </div>

        {/* LOADING */}
        {loading && (

          <div className="mt-12 text-center">

            <div className="w-14 h-14 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto" />

            <p className="mt-4 text-zinc-400">
              Processing your video...
            </p>

          </div>

        )}

        {/* VIDEO RESULT */}
        {video && !loading && (

          <div className="mt-16">

            <div className="bg-[#111113] border border-zinc-800 rounded-3xl p-6">

              <video
                controls
                className="w-full rounded-2xl"
                src={video}
              />

              <div className="mt-6 flex justify-between items-center">

                <div>

                  <h3 className="text-2xl font-bold">
                    Your AI Short is Ready 🚀
                  </h3>

                  <p className="text-zinc-400 mt-2">
                    Generated automatically with ClipForge AI
                  </p>

                </div>

                <button
                  onClick={() => {
                    window.location.href = video;
                  }}
                  className="bg-purple-600 hover:bg-purple-500 transition-all px-6 py-3 rounded-2xl font-semibold"
                >
                  Download
                </button>

              </div>

            </div>

          </div>

        )}

      </div>

    </div>
  );
}

export default App;