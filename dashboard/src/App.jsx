import { useState, useEffect } from "react";
import Background from "./Components/Background";
import Header from "./Components/Header";
import Layout from "./Components/Layout";
import Channels from "./Components/Channels";
import Graph from "./Components/Graph";
import BackToTop from "./Components/BackToTop";

const App = () => {
  const [selectedChannel, setSelectedChannel] = useState(null);
  const [showBackToTop, setShowBackToTop] = useState(false);

  useEffect(() => {
    const handleResize = () => {
        if (window.innerWidth < 1280) {
            setShowBackToTop(true);
        } else {
            setShowBackToTop(false);
        }
    };

    window.addEventListener("resize", handleResize);
    handleResize();
    return () => {
        window.removeEventListener("resize", handleResize);
    };
}, []);

  return (
    <main className="font-serif text-primary">
      <Background className="p-4">
        <Header />
        <Layout>
          <Channels selectedChannel={selectedChannel} setSelectedChannel={(channel_name) => setSelectedChannel(channel_name)}/>
          {showBackToTop && <BackToTop />}
          <Graph selectedChannel={selectedChannel}/>
        </Layout>
      </Background>
    </main>
  );
};

export default App;
