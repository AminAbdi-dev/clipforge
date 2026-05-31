
import {
  useState,
  useEffect,
  useRef
} from "react";

const API_URL =
  import.meta.env.VITE_API_URL;

function Dashboard() {
  const [menuOpen, setMenuOpen] =
  useState(false);
  const token = localStorage.getItem("token");
  

  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [videos, setVideos] = useState([]);
  const [shortCount, setShortCount] = useState(1);
  const [status, setStatus] = useState("");
  const [history, setHistory] = useState([]);
  const username =
  localStorage.getItem(
    "username"
  );
  const menuRef = useRef(null);


  const loadHistory = async () => {

    try {

      const response = await fetch(
  `${API_URL}/api/history/`,
  {
    headers: {
      Authorization:
        `Bearer ${localStorage.getItem("token")}`,
    },
  }
)

if (response.status === 401) {

  localStorage.removeItem("token");


  window.location.href = "/login";

  return;
}

      const data = await response.json();

      console.log("API HISTORY:", data);

      setHistory(data);

    } catch (error) {

      console.log(error);

    }

  };

  useEffect(() => {

    loadHistory();

  }, []);

  useEffect(() => {

    console.log("HISTORY:", history);

  }, [history]);

  useEffect(() => {

  const handleClickOutside = (
    event
  ) => {

    if (
      menuRef.current &&
      !menuRef.current.contains(
        event.target
      )
    ) {

      setMenuOpen(false);

    }

  };

  document.addEventListener(
    "mousedown",
    handleClickOutside
  );

  return () => {

    document.removeEventListener(
      "mousedown",
      handleClickOutside
    );

  };

}, []);
  

  const handleGenerate = async () => {

    if (!token) {

      alert("Please login first");

      return;
    }

    if (!url) return;

    setLoading(true);
    setStatus("Starting...");
    setVideos([]);

    try {

      setStatus("Sending request...");

      const response = await fetch(
        `${API_URL}/api/process/`,
        {
          method: "POST",
        headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
          body: JSON.stringify({
            youtube_url: url,
            short_count: shortCount,
          }),
        }
      );
    if (response.status === 401) {

    localStorage.removeItem("token");

    window.location.href = "/login";

    return;
    }

      const data = await response.json();

      console.log("API RESPONSE:", data);

      setStatus("Generating shorts...");

      if (data.success) {

        setStatus("Finalizing...");

        setVideos(
          data.videos.map(
            (video) =>
              `${API_URL}/media${video}`
          )
        );

        await loadHistory();

        setStatus("Done ✅");

      }

    } catch (error) {

      console.log(error);

      setStatus(
        "Error processing video"
      );

    }

    setLoading(false);

  };

const handleLogout = () => {

  localStorage.removeItem(
    "token"
  );

  localStorage.removeItem(
    "username"
  );

  window.location.href =
    "/login";
};


return (
  <div className="min-h-screen bg-[#07070a] text-white overflow-hidden">

    <div className="absolute top-[-200px] left-1/2 -translate-x-1/2 w-[700px] h-[700px] bg-purple-700 opacity-20 blur-[180px]" />

    <div className="relative z-10 max-w-6xl mx-auto px-6 py-20">

      <div
        ref={menuRef}
        className="relative"
      >

        <button
          onClick={() =>
            setMenuOpen(!menuOpen)
          }
          className="w-12 h-12 rounded-full bg-zinc-800 flex items-center justify-center text-xl hover:bg-zinc-700"
        >
          👤
        </button>

        {menuOpen && (

          <div className="absolute top-14 left-0 bg-zinc-900 border border-zinc-700 rounded-2xl p-4 w-52 shadow-xl z-50">

            <p className="font-semibold">
              {username}
            </p>

            <hr className="my-3 border-zinc-700" />

            <button
              onClick={handleLogout}
              className="text-red-400 hover:text-red-300"
            >
              Logout
            </button>

          </div>

        )}

      </div>

      <div className="text-center mt-10">

        <h1 className="text-7xl font-black tracking-tight bg-gradient-to-r from-white to-purple-400 bg-clip-text text-transparent">
          ClipForge
        </h1>

        <p className="text-zinc-400 mt-6 text-xl max-w-2xl mx-auto leading-relaxed">
          Transform long YouTube videos into viral AI-generated shorts with automatic clipping and subtitles.
        </p>

      </div>



        <div className="mt-16 bg-[#111113] border border-zinc-800 rounded-3xl p-8 shadow-2xl">

          <div className="flex flex-col md:flex-row gap-4">

            <input
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Paste YouTube URL..."
              className="flex-1 bg-[#1a1a1d] border border-zinc-700 rounded-2xl px-6 py-4 text-white outline-none focus:border-purple-500"
            />

            <select
              value={shortCount}
              onChange={(e) =>
                setShortCount(
                  Number(e.target.value)
                )
              }
              className="bg-[#1a1a1d] border border-zinc-700 rounded-2xl px-4 py-4 text-white"
            >
              <option value={1}>
                1 Short
              </option>

              <option value={3}>
                3 Shorts
              </option>

              <option value={5}>
                5 Shorts
              </option>

            </select>

            <button
              onClick={handleGenerate}
              className="bg-purple-600 hover:bg-purple-500 transition-all rounded-2xl px-8 py-4 font-semibold"
            >
              Generate Short
            </button>

          </div>

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

        {loading && (

          <div className="mt-12 text-center">

            <div className="w-14 h-14 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto" />

            <p className="mt-4 text-zinc-400">
              {status}
            </p>

          </div>

        )}

        {videos.length > 0 && !loading && (

          <div className="mt-16 space-y-8">

            {videos.map((video, index) => (

              <div
                key={index}
                className="bg-[#111113] border border-zinc-800 rounded-3xl p-6"
              >

                <video
                  controls
                  className="w-full rounded-2xl"
                  src={video}
                />

                <div className="mt-6 flex justify-between items-center">

                  <div>

                    <h3 className="text-2xl font-bold">
                      Short #{index + 1}
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

            ))}

          </div>

        )}
        {history.length > 0 && (

          <div className="mt-20">

            <h2 className="text-4xl font-bold mb-8">
              History
            </h2>

            <div className="space-y-6">

              {history.map((item, index) => (

                <div
                  key={index}
                  className="bg-[#111113] border border-zinc-800 rounded-3xl p-6"
                >

                  <h3 className="text-xl font-bold">
                    {item.title}
                  </h3>

                  <p className="text-zinc-500 mt-2">
                    {new Date(
                      item.created_at
                    ).toLocaleString()}
                  </p>

                  <button
                    onClick={() => {
                      window.open(
                        `${API_URL}/media${item.final_video}`
                      );
                    }}
                    className="mt-4 bg-purple-600 hover:bg-purple-500 transition-all px-6 py-3 rounded-2xl font-semibold"
                  >
                    Open Video
                  </button>

                </div>

              ))}

            </div>

          </div>

        )}

      </div>

    </div>

  );
}

export default Dashboard;
