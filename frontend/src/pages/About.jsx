import "../styles/about.css";

import workflowImage from "../assets/workflow/methodology_workflow.png";

function About() {

  return (

    <div className="about-page">

      <div className="about-title">

        <h1>
          About ParaVirPred
        </h1>

        <p>
          AI-Powered Parasite Virulence Prediction Platform
        </p>

      </div>

      <div className="about-card">

        <section className="about-section">

          <h2>
            🧬 The Biological Mandate & Motivation
          </h2>

          <p>

            Computational target identification is transforming modern
            drug discovery and precision medicine by enabling the rapid
            prioritization of biologically important proteins from
            large-scale genomic and proteomic datasets.

            Parasitic diseases caused by medically and economically
            significant protozoan pathogens continue to impose major
            public health and livestock production burdens worldwide.

            Traditional discovery of virulence factors, drug targets,
            and vaccine candidates depends heavily on labor-intensive,
            expensive, and time-consuming laboratory screening methods.

          </p>

          <p>

            Existing subtractive proteomics pipelines primarily rely on
            sequence similarity searches against host proteomes.
            Although useful, these approaches often fail to identify
            novel virulence-associated proteins that possess low
            sequence similarity but retain important structural or
            functional characteristics.

            ParaVirPred was developed to overcome these limitations by
            combining modern protein language models, structural
            bioinformatics, and machine learning into a unified
            high-throughput prediction framework.

          </p>

          <p>

            By leveraging deep biological representations learned from
            billions of protein sequences, the platform can recognize
            subtle evolutionary and structural patterns associated with
            pathogenicity and virulence, enabling rapid proteome-scale
            screening of parasite proteins.

          </p>

        </section>

        <section className="about-section">

          <h2>
            🖥️ Architectural Framework & Technical Specifications
          </h2>

          <p>

            The computational architecture of ParaVirPred moves beyond
            conventional alignment-based approaches and adopts a
            multi-modal machine learning framework integrating deep
            biological representations with classical biochemical
            descriptors.

          </p>

          <ul>

            <li>

              <span className="about-highlight">
                ProtT5-XL-UniRef50
              </span>

              {" "}
              generates 1024-dimensional embeddings capturing
              evolutionary, structural, and functional information
              directly from protein sequences.

            </li>

            <li>

              <span className="about-highlight">
                ESM-2
              </span>

              {" "}
              provides 1280-dimensional transformer-based
              representations that capture residue-level context,
              structural constraints, active sites, and protein
              interaction patterns.

            </li>

            <li>

              <span className="about-highlight">
                Physicochemical Features
              </span>

              {" "}
              complement deep embeddings through biologically
              interpretable descriptors such as molecular weight,
              aromaticity, instability index, isoelectric point,
              GRAVY score, AlphaFold confidence, pocket depth,
              and pocket volume.

            </li>

          </ul>

          <p>

            The integration of language model embeddings and
            physicochemical descriptors enables the system to capture
            both learned biological semantics and experimentally
            interpretable molecular characteristics.

          </p>

        </section>

        <section className="about-section">

          <h2>
            📊 Benchmarking Framework & Performance Topology
          </h2>

          <p>

            ParaVirPred was developed and evaluated using a curated
            benchmark dataset containing approximately 8,928 protein
            profiles representing virulent and non-virulent classes.

          </p>

          <p>

            Multiple machine learning algorithms were systematically
            compared, including Logistic Regression, Support Vector
            Machines (SVM), Random Forest, XGBoost, Multi-Layer
            Perceptron (MLP), Naive Bayes, K-Nearest Neighbors (KNN),
            and Deep Neural Networks (DNN).

          </p>

          <p>

            Six distinct feature combinations involving ProtT5
            embeddings, ESM2 embeddings, physicochemical descriptors,
            and hybrid feature spaces were benchmarked using extensive
            validation experiments.

          </p>

          <p>

            The combination of
            <span className="about-highlight">
              {" "}ProtT5 Embeddings + Physicochemical Features
            </span>
            {" "}
            consistently emerged as the best-performing feature space,
            while SVM and DNN architectures demonstrated superior
            predictive capability across multiple evaluation metrics
            including MCC, Accuracy, Sensitivity, Specificity,
            Precision, and F1 Score.

          </p>

        </section>

        <section className="about-section">

          <h2>
            🗺️ Unified Methodology Workflow
          </h2>

          <p>

            The complete ParaVirPred workflow integrates large-scale
            parasite proteome analysis with deep representation
            learning, machine learning classification, structural
            validation, and downstream target prioritization.

          </p>

          <div className="workflow-container">

            <img
              src={workflowImage}
              alt="Methodology Workflow"
              className="workflow-image"
            />

            <p className="workflow-caption">

              The workflow consists of four major phases:
              input proteome acquisition, multi-modal feature
              engineering, virulence classification using optimized
              machine learning models, and downstream subtractive
              proteomics analyses including host non-homology,
              essentiality assessment, AlphaFold structural validation,
              and binding pocket characterization.

            </p>

          </div>

        </section>

      </div>

    </div>

  );

}

export default About;