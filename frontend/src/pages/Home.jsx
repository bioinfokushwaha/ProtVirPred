import NIABBanner from "../components/NIABBanner";
import HeroSection from "../components/HeroSection";
import FeatureCard from "../components/FeatureCard";

import { useNavigate } from "react-router-dom";

function Home() {

  const navigate = useNavigate();

  return (

    <>

      <NIABBanner />

      <HeroSection />

      <section className="features-section">

        <h2>
          Features
        </h2>

        <div className="features-grid">

          <div
            onClick={() => navigate("/about")}
            style={{ cursor: "pointer" }}
          >
            <FeatureCard
              icon="📚"
              title="Dataset"
              description="Benchmark training and independent test datasets used for model development."
            />
          </div>

          <div
            onClick={() => navigate("/help")}
            style={{ cursor: "pointer" }}
          >
            <FeatureCard
              icon="🤖"
              title="AI Models"
              description="Protein language models, physicochemical descriptors and machine learning architectures."
            />
          </div>

          <div
            onClick={() => navigate("/prediction")}
            style={{ cursor: "pointer" }}
          >
            <FeatureCard
              icon="🔬"
              title="Prediction"
              description="Explore model combinations and virulence prediction workflows."
            />
          </div>

          <div
            onClick={() => navigate("/download")}
            style={{ cursor: "pointer" }}
          >
            <FeatureCard
              icon="⚙️"
              title="Process Data"
              description="Download datasets, trained models and standalone prediction pipelines."
            />
          </div>

        </div>

      </section>

      <section className="about-platform">

        <h2>
          About ParaVirPred
        </h2>

        <p>

          ParaVirPred is an AI-driven
          parasite virulence prediction
          webserver.

        </p>

        <p>

          The platform combines
          protein language models
          including ESM2 and ProtT5
          with physicochemical features
          and machine learning models
          to identify virulent proteins.

        </p>

      </section>

    </>

  );

}

export default Home;