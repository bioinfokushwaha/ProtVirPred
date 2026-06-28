import paraVirPredLogo from "../assets/logos/paravirpred-logo.png";

function HeroSection() {

  return (

    <section className="hero">

      <div className="hero-overlay">

        <img
          src={paraVirPredLogo}
          alt="ParaVirPred Logo"
          className="hero-app-logo"
        />

        <h2>
          AI-Based Parasite Virulence Prediction WebServer 
        </h2>

        <p>

          Advanced bioinformatics platform
          for identifying virulence-associated
          proteins using protein language models,
          physicochemical features and
          machine learning.

        </p>

        <p>

          Supporting large-scale parasite
          protein analysis through ESM2,
          ProtT5 and hybrid AI models.

        </p>

      </div>

    </section>

  );

}

export default HeroSection;